"""Note Pydantic models for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Schema for creating a new note."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = ""
    tags: list[str] = Field(default_factory=list)
    pinned: bool = False
    folder_id: Optional[str] = None


class NoteUpdate(BaseModel):
    """Schema for updating a note."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    tags: Optional[list[str]] = None
    pinned: Optional[bool] = None
    folder_id: Optional[str] = None


class NoteResponse(BaseModel):
    """Schema returned to the client for note data."""

    id: str
    user_id: str
    title: str
    content: str
    tags: list[str]
    pinned: bool
    folder_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
