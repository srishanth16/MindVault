"""FastAPI dependency that extracts and validates the current user from JWT."""

from fastapi import Header, HTTPException, status
from jose import JWTError

from app.services.auth_service import decode_access_token


async def get_current_user(authorization: str = Header(...)) -> str:
    """Extract the Bearer token from the Authorization header and return the user ID.

    Raises:
        HTTPException 401: If the header is missing, malformed, or the token is invalid.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'.",
        )

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload missing subject claim.",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )
