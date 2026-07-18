"""File handling utilities for uploads."""

import os
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import settings

# Map of extensions to logical type names
_EXTENSION_MAP: dict[str, str] = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "docx",
    ".txt": "txt",
    ".pptx": "pptx",
    ".ppt": "pptx",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".gif": "image",
    ".webp": "image",
    ".svg": "image",
    ".bmp": "image",
}


def _ensure_upload_dir(user_id: str) -> Path:
    """Create the user-specific upload directory if it does not exist."""
    upload_path = Path(settings.UPLOAD_DIR) / user_id
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


async def save_upload_file(file: UploadFile, user_id: str) -> tuple[str, int]:
    """Save an uploaded file to disk under ``uploads/{user_id}/``.

    The file is stored with a UUID prefix to avoid name collisions.

    Returns:
        A tuple of (relative file path, file size in bytes).
    """
    upload_dir = _ensure_upload_dir(user_id)

    # Preserve the original extension but add a UUID prefix
    ext = Path(file.filename or "file").suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest = upload_dir / unique_name

    # Stream the file to disk
    size = 0
    with open(dest, "wb") as buffer:
        while chunk := await file.read(1024 * 64):  # 64 KB chunks
            buffer.write(chunk)
            size += len(chunk)

    return str(dest), size


def delete_file(file_path: str) -> bool:
    """Delete a file from disk.

    Returns:
        True if the file was deleted, False if it did not exist.
    """
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    except OSError:
        return False


def get_file_type(filename: str) -> str:
    """Determine the logical file type from a filename's extension.

    Returns one of: ``pdf``, ``docx``, ``txt``, ``pptx``, ``image``, ``other``.
    """
    ext = Path(filename).suffix.lower()
    return _EXTENSION_MAP.get(ext, "other")
