"""Vector database integration using Qdrant."""

from typing import Any, Dict, List, Optional
import os

# Move all heavy imports inside functions to prevent hanging at import time!
# from langchain_qdrant import QdrantVectorStore
# from langchain_core.documents import Document
# from langchain_openai import OpenAIEmbeddings
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams
# from qdrant_client import models

from app.config import settings

# In a real app, you might connect to a Qdrant cloud instance or a local docker container.
# For simplicity, we use an in-memory client if no URL is provided, or connect to the given URL.
QDRANT_URL = os.getenv("QDRANT_URL", None)
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

# Lazy initialization
_client = None
_embeddings = None
_collection_initialized = False
COLLECTION_NAME = "mindvault_docs"


def get_client():
    from qdrant_client import QdrantClient
    global _client
    if _client is None:
        if QDRANT_URL:
            _client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        else:
            _client = QdrantClient(":memory:")
    return _client


def get_embeddings():
    from langchain_openai import OpenAIEmbeddings
    global _embeddings
    if _embeddings is None:
        try:
            _embeddings = OpenAIEmbeddings()
        except Exception as e:
            print(f"Warning: Could not initialize OpenAIEmbeddings: {e}. AI features may not work.")
            _embeddings = None  # or use dummy embeddings?
    return _embeddings


def initialize_collection():
    """Ensure the collection exists in Qdrant."""
    from qdrant_client.models import Distance, VectorParams
    global _collection_initialized
    if _collection_initialized:
        return
    client = get_client()
    try:
        collections = client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
        _collection_initialized = True
    except Exception as e:
        print(f"Warning: Could not initialize Qdrant collection: {e}. AI features may not work.")


def get_vector_store():
    from langchain_qdrant import QdrantVectorStore
    """Return a LangChain Qdrant vector store instance."""
    client = get_client()
    embeddings = get_embeddings()
    if embeddings is None:
        return None
    initialize_collection()
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings,
    )


def add_documents_to_store(documents: List):
    """Add a list of LangChain documents to the vector store."""
    vector_store = get_vector_store()
    if vector_store is None:
        return []
    return vector_store.add_documents(documents)


def delete_document_from_store(doc_id: str) -> None:
    """Delete a document from Qdrant by its ID. 
    Note: Requires filtering by metadata if chunks are stored.
    """
    from qdrant_client import models
    try:
        client = get_client()
        initialize_collection()
        # Assuming doc_id is stored in metadata["source_doc_id"]
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.source_doc_id",
                        match=models.MatchValue(value=doc_id)
                    )
                ]
            )
        )
    except Exception as e:
        print(f"Warning: Could not delete document from vector store: {e}")
