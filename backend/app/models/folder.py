"""Folder Pydantic models for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FolderCreate(BaseModel):
    """Schema for creating a new folder."""

    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[str] = None


class FolderResponse(BaseModel):
    """Schema returned to the client for folder data."""

    id: str
    user_id: str
    name: str
    parent_id: Optional[str] = None
    created_at: datetime
