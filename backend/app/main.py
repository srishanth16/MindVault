from contextlib import asynccontextmanager
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, documents, folders, notes, stats, chat, search
from app.database import close_connection, create_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        create_indexes()
    except Exception as e:
        print(f"WARNING: Error during startup (create_indexes): {e}", file=sys.stderr)
    yield
    # Shutdown
    try:
        close_connection()
    except Exception as e:
        print(f"WARNING: Error during shutdown (close_connection): {e}", file=sys.stderr)


app = FastAPI(
    title="MindVault API",
    description="AI Powered Personal Knowledge Brain API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(notes.router)
app.include_router(folders.router)
app.include_router(stats.router)
app.include_router(chat.router)
app.include_router(search.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
