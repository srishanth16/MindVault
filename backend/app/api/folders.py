"""Folder management routes: CRUD with cascade delete."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_database
from app.middleware.auth_middleware import get_current_user
from app.models.folder import FolderCreate, FolderResponse

router = APIRouter(prefix="/api/folders", tags=["Folders"])


def _folder_to_response(doc: dict) -> FolderResponse:
    """Convert a MongoDB folder document to a FolderResponse."""
    return FolderResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        name=doc["name"],
        parent_id=doc.get("parent_id"),
        created_at=doc["created_at"],
    )


@router.get("/", response_model=list[FolderResponse])
async def list_folders(user_id: str = Depends(get_current_user)):
    """List all folders belonging to the current user.

    Results are sorted by creation date (newest first).
    """
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")
    folders = db.folders.find({"user_id": user_id}).sort("created_at", -1)
    return [_folder_to_response(f) for f in folders]


@router.post("/", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(body: FolderCreate, user_id: str = Depends(get_current_user)):
    """Create a new folder, optionally nested under a parent folder."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    # Validate parent exists if provided
    if body.parent_id is not None:
        parent = db.folders.find_one(
            {"_id": ObjectId(body.parent_id), "user_id": user_id}
        )
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent folder not found.",
            )

    now = datetime.now(timezone.utc)
    folder_doc = {
        "user_id": user_id,
        "name": body.name,
        "parent_id": body.parent_id,
        "created_at": now,
    }

    result = db.folders.insert_one(folder_doc)
    folder_doc["_id"] = result.inserted_id
    return _folder_to_response(folder_doc)


@router.put("/{folder_id}", response_model=FolderResponse)
async def rename_folder(
    folder_id: str,
    body: FolderCreate,
    user_id: str = Depends(get_current_user),
):
    """Rename a folder."""
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    result = db.folders.find_one_and_update(
        {"_id": ObjectId(folder_id), "user_id": user_id},
        {"$set": {"name": body.name}},
        return_document=True,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found.",
        )

    return _folder_to_response(result)


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(folder_id: str, user_id: str = Depends(get_current_user)):
    """Delete a folder and cascade-remove its contents.

    All documents and notes inside the folder are moved to the root
    (folder_id set to None). Child folders are also deleted recursively.
    """
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    folder = db.folders.find_one({"_id": ObjectId(folder_id), "user_id": user_id})
    if folder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found.",
        )

    # Move contained documents and notes to root
    db.documents.update_many(
        {"user_id": user_id, "folder_id": folder_id},
        {"$set": {"folder_id": None}},
    )
    db.notes.update_many(
        {"user_id": user_id, "folder_id": folder_id},
        {"$set": {"folder_id": None}},
    )

    # Delete child folders recursively
    _delete_child_folders(db, user_id, folder_id)

    # Delete the folder itself
    db.folders.delete_one({"_id": ObjectId(folder_id)})


def _delete_child_folders(db, user_id: str, parent_id: str) -> None:
    """Recursively delete all child folders under a given parent."""
    children = db.folders.find({"user_id": user_id, "parent_id": parent_id})
    for child in children:
        child_id = str(child["_id"])
        # Move contents of child folder to root
        db.documents.update_many(
            {"user_id": user_id, "folder_id": child_id},
            {"$set": {"folder_id": None}},
        )
        db.notes.update_many(
            {"user_id": user_id, "folder_id": child_id},
            {"$set": {"folder_id": None}},
        )
        _delete_child_folders(db, user_id, child_id)
        db.folders.delete_one({"_id": child["_id"]})
