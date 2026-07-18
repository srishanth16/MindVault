"""AI service for document processing and chat using LangChain, OpenAI, and PyMuPDF."""

import os
from typing import List

import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.vector_db import add_documents_to_store, get_vector_store

# Lazy initialization
_chat_model = None
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)


def get_chat_model():
    from langchain_openai import ChatOpenAI
    global _chat_model
    if _chat_model is None:
        try:
            _chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        except Exception as e:
            print(f"Warning: Could not initialize ChatOpenAI: {e}. AI features may not work.")
            _chat_model = None
    return _chat_model


def process_document(file_path: str, doc_id: str, title: str) -> int:
    from langchain_core.documents import Document
    """Extract text from a document, split it, and store in vector db.
    Returns the number of chunks stored.
    """
    text = ""
    # Use PyMuPDF for PDF extraction
    if file_path.lower().endswith(".pdf"):
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text() + "\n"
    else:
        # Fallback to plain text reading
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            text = f"Error reading file: {str(e)}"

    if not text.strip():
        return 0

    # Split text into chunks
    chunks = text_splitter.split_text(text)

    # Create LangChain documents with metadata
    documents = [
        Document(
            page_content=chunk,
            metadata={
                "source_doc_id": doc_id,
                "title": title,
                "chunk_index": i
            }
        )
        for i, chunk in enumerate(chunks)
    ]

    # Store in vector db
    add_documents_to_store(documents)

    return len(documents)


def ask_question(query: str, user_id: str) -> str:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.documents import Document
    """Answer a user's question using RAG over their documents."""
    vector_store = get_vector_store()
    chat_model = get_chat_model()
    if vector_store is None or chat_model is None:
        return "AI features are not available. Please check your OpenAI API key."

    # We retrieve relevant documents. Note: Ideally we filter by user_id
    # Since Qdrant supports payload filtering, we would add that, but for now
    # we just retrieve based on similarity.
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs: List[Document]):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | chat_model
        | StrOutputParser()
    )

    try:
        return chain.invoke(query)
    except Exception as e:
        return f"Error generating response: {str(e)}"
