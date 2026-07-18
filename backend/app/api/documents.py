"""Document management routes: upload, list, search, update, delete."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status

from app.database import get_database
from app.middleware.auth_middleware import get_current_user
from app.models.document import DocumentResponse, DocumentUpdate
from app.services.file_service import delete_file, get_file_type, save_upload_file

router = APIRouter(prefix="/api/documents", tags=["Documents"])


def _doc_to_response(doc: dict) -> DocumentResponse:
    """Convert a MongoDB document to a DocumentResponse."""
    return DocumentResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        title=doc["title"],
        type=doc["type"],
        size=doc["size"],
        folder_id=doc.get("folder_id"),
        file_path=doc["file_path"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    folder_id: Optional[str] = Query(None, description="Filter by folder ID"),
    type: Optional[str] = Query(None, description="Filter by file type"),
    user_id: str = Depends(get_current_user),
):
    """List all documents belonging to the current user.

    Supports optional filtering by folder and file type.
    Results are sorted by creation date (newest first).
    """
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    query: dict = {"user_id": user_id}

    if folder_id is not None:
        query["folder_id"] = folder_id
    if type is not None:
        query["type"] = type

    docs = db.documents.find(query).sort("created_at", -1)
    return [_doc_to_response(doc) for doc in docs]


@router.post("/upload", response_model=list[DocumentResponse], status_code=status.HTTP_201_CREATED)
async def upload_documents(
    files: list[UploadFile] = File(...),
    folder_id: Optional[str] = Form(None),
    user_id: str = Depends(get_current_user),
):
    """Upload one or more files.

    Each file is saved to disk and a corresponding document record is created in MongoDB.
    """
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    now = datetime.now(timezone.utc)
    created: list[DocumentResponse] = []

    for file in files:
        file_path, size = await save_upload_file(file, user_id)
        file_type = get_file_type(file.filename or "unknown")

        doc = {
            "user_id": user_id,
            "title": file.filename or "Untitled",
            "type": file_type,
            "size": size,
            "folder_id": folder_id,
            "file_path": file_path,
            "created_at": now,
            "updated_at": now,
        }

        result = db.documents.insert_one(doc)
        doc["_id"] = result.inserted_id
        created.append(_doc_to_response(doc))

    return created


@router.get("/search", response_model=list[DocumentResponse])
async def search_documents(
    q: str = Query(..., min_length=1, description="Search keyword"),
    user_id: str = Depends(get_current_user),
):
    """Search the current user's documents by keyword in the title.

    Uses MongoDB text index for full-text search.
    """
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    docs = (
        db.documents.find({"user_id": user_id, "$text": {"$search": q}})
        .sort("created_at", -1)
    )
    return [_doc_to_response(doc) for doc in docs]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, user_id: str = Depends(get_current_user)):
    """Retrieve a single document by its ID."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    doc = db.documents.find_one({"_id": ObjectId(document_id), "user_id": user_id})

    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return _doc_to_response(doc)


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    body: DocumentUpdate,
    user_id: str = Depends(get_current_user),
):
    """Update a document's title or move it to a different folder."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    update_fields: dict = {"updated_at": datetime.now(timezone.utc)}
    if body.title is not None:
        update_fields["title"] = body.title
    if body.folder_id is not None:
        update_fields["folder_id"] = body.folder_id

    result = db.documents.find_one_and_update(
        {"_id": ObjectId(document_id), "user_id": user_id},
        {"$set": update_fields},
        return_document=True,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return _doc_to_response(result)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, user_id: str = Depends(get_current_user)):
    """Delete a document record and its associated file from disk."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    doc = db.documents.find_one_and_delete(
        {"_id": ObjectId(document_id), "user_id": user_id}
    )

    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    # Best-effort file deletion
    delete_file(doc.get("file_path", ""))
