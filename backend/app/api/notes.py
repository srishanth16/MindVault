"""Note management routes: CRUD with filtering."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_database
from app.middleware.auth_middleware import get_current_user
from app.models.note import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/api/notes", tags=["Notes"])


def _note_to_response(doc: dict) -> NoteResponse:
    """Convert a MongoDB note document to a NoteResponse."""
    return NoteResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        title=doc["title"],
        content=doc.get("content", ""),
        tags=doc.get("tags", []),
        pinned=doc.get("pinned", False),
        folder_id=doc.get("folder_id"),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


@router.get("/", response_model=list[NoteResponse])
async def list_notes(
    folder_id: Optional[str] = Query(None, description="Filter by folder ID"),
    pinned: Optional[bool] = Query(None, description="Filter pinned notes"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    user_id: str = Depends(get_current_user),
):
    """List all notes belonging to the current user.

    Supports optional filtering by folder, pinned status, and tag.
    Results are sorted by creation date (newest first).
    """
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    query: dict = {"user_id": user_id}

    if folder_id is not None:
        query["folder_id"] = folder_id
    if pinned is not None:
        query["pinned"] = pinned
    if tag is not None:
        query["tags"] = tag  # MongoDB matches if the array contains this value

    notes = db.notes.find(query).sort("created_at", -1)
    return [_note_to_response(note) for note in notes]


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(body: NoteCreate, user_id: str = Depends(get_current_user)):
    """Create a new note."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    now = datetime.now(timezone.utc)

    note_doc = {
        "user_id": user_id,
        "title": body.title,
        "content": body.content,
        "tags": body.tags,
        "pinned": body.pinned,
        "folder_id": body.folder_id,
        "created_at": now,
        "updated_at": now,
    }

    result = db.notes.insert_one(note_doc)
    note_doc["_id"] = result.inserted_id
    return _note_to_response(note_doc)


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str, user_id: str = Depends(get_current_user)):
    """Retrieve a single note by its ID."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    note = db.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )

    return _note_to_response(note)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    body: NoteUpdate,
    user_id: str = Depends(get_current_user),
):
    """Update a note's title, content, tags, pinned status, or folder."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    update_fields: dict = {"updated_at": datetime.now(timezone.utc)}
    if body.title is not None:
        update_fields["title"] = body.title
    if body.content is not None:
        update_fields["content"] = body.content
    if body.tags is not None:
        update_fields["tags"] = body.tags
    if body.pinned is not None:
        update_fields["pinned"] = body.pinned
    if body.folder_id is not None:
        update_fields["folder_id"] = body.folder_id

    result = db.notes.find_one_and_update(
        {"_id": ObjectId(note_id), "user_id": user_id},
        {"$set": update_fields},
        return_document=True,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )

    return _note_to_response(result)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, user_id: str = Depends(get_current_user)):
    """Delete a note by its ID."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    result = db.notes.delete_one({"_id": ObjectId(note_id), "user_id": user_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )
