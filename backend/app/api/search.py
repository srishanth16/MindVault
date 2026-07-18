"""Semantic search API."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.middleware.auth_middleware import get_current_user
from app.services.vector_db import get_vector_store

router = APIRouter(prefix="/api/search", tags=["Semantic Search"])

class SearchResult(BaseModel):
    content: str
    source_doc_id: str
    title: str
    score: float

@router.get("/semantic", response_model=list[SearchResult])
async def semantic_search(
    q: str = Query(..., min_length=1, description="Semantic search query"),
    user_id: str = Depends(get_current_user),
):
    """Search for relevant document snippets based on semantic similarity."""
    try:
        vector_store = get_vector_store()
        # Retrieve top 5 most similar chunks
        results = vector_store.similarity_search_with_score(q, k=5)
        
        # Format the response
        response = []
        for doc, score in results:
            response.append(
                SearchResult(
                    content=doc.page_content,
                    source_doc_id=doc.metadata.get("source_doc_id", "unknown"),
                    title=doc.metadata.get("title", "Unknown Title"),
                    score=float(score)
                )
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )
