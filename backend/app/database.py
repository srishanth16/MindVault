"""MongoDB connection and index management."""

from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.database import Database
from pymongo.errors import ConfigurationError, ConnectionFailure
import sys

from app.config import settings

_client: MongoClient | None = None


def get_client() -> MongoClient | None:
    """Return the global MongoClient, creating it on first call.

    Returns None if connection fails.
    """
    global _client
    if _client is None:
        try:
            _client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
            # Verify the connection
            _client.admin.command("ping")
            print("Successfully connected to MongoDB!")
        except (ConfigurationError, ConnectionFailure) as e:
            print(f"WARNING: Could not connect to MongoDB! Error: {e}", file=sys.stderr)
            print("The app will run, but database features will not be available.", file=sys.stderr)
            _client = None
    return _client


def get_database() -> Database | None:
    """Return the MindVault database instance, or None if no connection."""
    client = get_client()
    if client is None:
        return None
    return client.get_default_database("mindvault")


def create_indexes() -> None:
    """Create required indexes for all collections.

    Called once at application startup.
    """
    db = get_database()
    if db is None:
        print("Skipping index creation (no MongoDB connection)", file=sys.stderr)
        return

    try:
        # Users – unique email
        db.users.create_index([("email", ASCENDING)], unique=True)
        print("Created index on users.email")

        # Documents – lookup by user, text search on title
        db.documents.create_index([("user_id", ASCENDING)])
        db.documents.create_index([("title", TEXT)])
        print("Created indexes on documents")

        # Notes – lookup by user, text search on title
        db.notes.create_index([("user_id", ASCENDING)])
        db.notes.create_index([("title", TEXT)])
        print("Created indexes on notes")

        # Folders – lookup by user
        db.folders.create_index([("user_id", ASCENDING)])
        print("Created indexes on folders")
        print("All indexes created successfully!")
    except Exception as e:
        print(f"WARNING: Could not create MongoDB indexes! Error: {e}", file=sys.stderr)


def close_connection() -> None:
    """Close the global MongoClient."""
    global _client
    if _client is not None:
        try:
            _client.close()
            print("Closed MongoDB connection.")
        except Exception:
            pass
        _client = None
