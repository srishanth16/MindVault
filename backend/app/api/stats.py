"""Dashboard statistics route."""

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_database
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api", tags=["Statistics"])


@router.get("/stats", response_model=dict)
async def get_stats(user_id: str = Depends(get_current_user)):
    """Return aggregate counts and storage usage for the current user.

    Response:
        - documents: total document count
        - notes: total note count
        - folders: total folder count
        - storage_used: sum of all document sizes in bytes
    """
    db = get_database()
    if db is None:
        raise HTTPException(503, "Database connection unavailable.")

    documents_count = db.documents.count_documents({"user_id": user_id})
    notes_count = db.notes.count_documents({"user_id": user_id})
    folders_count = db.folders.count_documents({"user_id": user_id})

    # Aggregate total storage used across all documents
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": None, "total_size": {"$sum": "$size"}}},
    ]
    storage_result = list(db.documents.aggregate(pipeline))
    storage_used = storage_result[0]["total_size"] if storage_result else 0

    return {
        "documents": documents_count,
        "notes": notes_count,
        "folders": folders_count,
        "storage_used": storage_used,
    }
