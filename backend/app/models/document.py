"""Document Pydantic models for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """Schema returned to the client for document data."""

    id: str
    user_id: str
    title: str
    type: str
    size: int
    folder_id: Optional[str] = None
    file_path: str
    created_at: datetime
    updated_at: datetime


class DocumentUpdate(BaseModel):
    """Schema for updating a document's metadata."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    folder_id: Optional[str] = None
