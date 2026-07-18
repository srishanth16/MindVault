"""Chat API using LangChain RAG."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.middleware.auth_middleware import get_current_user
from app.services.ai_service import ask_question

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
async def chat_with_docs(
    body: ChatRequest,
    user_id: str = Depends(get_current_user),
):
    """Ask a question to the AI, which will use the user's documents as context."""
    if not body.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty."
        )
    
    try:
        reply = ask_question(body.message, user_id)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )
