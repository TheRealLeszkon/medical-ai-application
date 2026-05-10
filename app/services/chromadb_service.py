"""
ChromaDB service for storing and querying medical document embeddings.
Uses ChromaDB's built-in embedding function (Sentence Transformers).
"""

import chromadb
from chromadb.config import Settings
import os

# Persistent ChromaDB storage directory
CHROMA_PERSIST_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "chroma_data"
)

# Initialize ChromaDB client with persistent storage
chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

# Get or create the medical documents collection
# ChromaDB uses its default embedding function (all-MiniLM-L6-v2)
collection = chroma_client.get_or_create_collection(
    name="medical_documents",
    metadata={"hnsw:space": "cosine"}
)


def add_document_embedding(
    document_id: str,
    text: str,
    patient_id: int,
    document_name: str
) -> str:
    """
    Add a document's text to ChromaDB as an embedding.
    
    Args:
        document_id: Unique ID for the document (e.g., "doc_123")
        text: The extracted text content from the document
        patient_id: The patient this document belongs to
        document_name: Original filename of the document
    
    Returns:
        The document_id used in ChromaDB
    """
    chroma_doc_id = f"doc_{document_id}"

    collection.upsert(
        ids=[chroma_doc_id],
        documents=[text],
        metadatas=[{
            "patient_id": str(patient_id),
            "document_name": document_name,
            "document_id": str(document_id)
        }]
    )

    return chroma_doc_id


def query_documents(
    query_text: str,
    patient_id: int | None = None,
    n_results: int = 5
) -> dict:
    """
    Query ChromaDB for the most relevant documents.
    
    Args:
        query_text: The search query or question
        patient_id: Optional patient ID to filter results
        n_results: Number of results to return
    
    Returns:
        Dict with ids, documents, distances, and metadatas
    """
    where_filter = None
    if patient_id is not None:
        where_filter = {"patient_id": str(patient_id)}

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where_filter if where_filter else None
    )

    return results


def get_all_documents_for_patient(patient_id: int) -> dict:
    """
    Retrieve all stored documents for a given patient from ChromaDB.
    """
    results = collection.get(
        where={"patient_id": str(patient_id)}
    )
    return results


def delete_document(document_id: str):
    """Delete a document from ChromaDB."""
    chroma_doc_id = f"doc_{document_id}"
    try:
        collection.delete(ids=[chroma_doc_id])
    except Exception:
        pass
