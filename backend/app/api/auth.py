"""Authentication routes: register, login, profile."""

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_database
from app.middleware.auth_middleware import get_current_user
from app.models.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services.auth_service import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def _user_doc_to_response(doc: dict) -> UserResponse:
    """Convert a MongoDB user document to a UserResponse."""
    return UserResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        email=doc["email"],
        avatar_url=doc.get("avatar_url"),
        created_at=doc["created_at"],
    )


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate):
    """Register a new user account.

    Returns a JWT access token and user profile on success.
    Raises 409 if the email is already registered.
    """
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable.",
        )

    # Check for existing email
    if db.users.find_one({"email": body.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    now = datetime.now(timezone.utc)
    user_doc = {
        "name": body.name,
        "email": body.email,
        "password_hash": hash_password(body.password),
        "avatar_url": None,
        "created_at": now,
        "updated_at": now,
    }

    result = db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    token = create_access_token(str(result.inserted_id))
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": _user_doc_to_response(user_doc).model_dump(),
    }


@router.post("/login", response_model=dict)
async def login(body: UserLogin):
    """Authenticate a user with email and password.

    Returns a JWT access token and user profile on success.
    Raises 401 on invalid credentials.
    """
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable.",
        )
    user_doc = db.users.find_one({"email": body.email})

    if user_doc is None or not verify_password(body.password, user_doc["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token(str(user_doc["_id"]))
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": _user_doc_to_response(user_doc).model_dump(),
    }


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: str = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable.",
        )
    user_doc = db.users.find_one({"_id": ObjectId(user_id)})

    if user_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return _user_doc_to_response(user_doc)


@router.put("/profile", response_model=UserResponse)
async def update_profile(body: UserUpdate, user_id: str = Depends(get_current_user)):
    """Update the authenticated user's name and/or avatar URL."""
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable.",
        )

    update_fields: dict = {"updated_at": datetime.now(timezone.utc)}
    if body.name is not None:
        update_fields["name"] = body.name
    if body.avatar_url is not None:
        update_fields["avatar_url"] = body.avatar_url

    result = db.users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields},
        return_document=True,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return _user_doc_to_response(result)
