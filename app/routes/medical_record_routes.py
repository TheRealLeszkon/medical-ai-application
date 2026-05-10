"""
Medical record routes - handles file upload (PDF/images),
text extraction, ChromaDB embedding, and document retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from sqlmodel import Session, select

from app.database import get_session
from app.models import MedicalDocument
from app.services.chromadb_service import (
    add_document_embedding,
    query_documents,
    get_all_documents_for_patient,
)
from app.services.openrouter_service import extract_text_from_image

import pypdf
import io


router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"]
)


def _extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using PyPDF."""
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n\n".join(text_parts)


# -------------------------
# UPLOAD DOCUMENT (PDF or Image)
# -------------------------
@router.post("/upload")
async def upload_medical_record(
    patient_id: int = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """
    Upload a medical document (PDF or image).
    - PDFs: text is extracted using PyPDF
    - Images: text is extracted using OpenRouter vision model (OCR)
    - Extracted text is embedded in ChromaDB
    - File binary is stored in PostgreSQL
    """
    # Validate file type
    allowed_types = [
        "application/pdf",
        "image/png", "image/jpeg", "image/jpg",
        "image/webp", "image/gif"
    ]

    content_type = file.content_type or "application/octet-stream"

    if content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {content_type}. "
                   f"Allowed: PDF, PNG, JPEG, WebP, GIF"
        )

    # Read file bytes
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    # Extract text based on file type
    extracted_text = ""
    try:
        if content_type == "application/pdf":
            extracted_text = _extract_text_from_pdf(file_bytes)
        else:
            # Image file - use OpenRouter OCR
            extracted_text = extract_text_from_image(
                image_bytes=file_bytes,
                mime_type=content_type
            )
    except Exception as e:
        # Store the document even if text extraction fails
        extracted_text = f"[Text extraction failed: {str(e)}]"

    if not extracted_text.strip():
        extracted_text = "[No text could be extracted from this document]"

    # Save to PostgreSQL
    document = MedicalDocument(
        document_name=file.filename or "untitled",
        patient_id=patient_id,
        file_type=content_type,
        file_data=file_bytes,
        extracted_text=extracted_text,
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    # Add to ChromaDB
    chroma_id = add_document_embedding(
        document_id=str(document.document_id),
        text=extracted_text,
        patient_id=patient_id,
        document_name=document.document_name
    )

    # Update the vector embedding ID
    document.vector_embedding_id = chroma_id
    session.commit()
    session.refresh(document)

    return {
        "message": "Document uploaded and processed successfully",
        "document_id": document.document_id,
        "document_name": document.document_name,
        "patient_id": patient_id,
        "file_type": content_type,
        "text_preview": extracted_text[:500] + ("..." if len(extracted_text) > 500 else ""),
        "chroma_id": chroma_id
    }


# -------------------------
# GET DOCUMENT METADATA
# -------------------------
@router.get("/{document_id}")
def get_document(
    document_id: int,
    session: Session = Depends(get_session)
):
    document = session.get(MedicalDocument, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "document_id": document.document_id,
        "document_name": document.document_name,
        "patient_id": document.patient_id,
        "file_type": document.file_type,
        "extracted_text": document.extracted_text,
        "vector_embedding_id": document.vector_embedding_id,
        "uploaded_at": str(document.uploaded_at) if document.uploaded_at else None,
        "has_file": document.file_data is not None
    }


# -------------------------
# DOWNLOAD ORIGINAL FILE
# -------------------------
@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    session: Session = Depends(get_session)
):
    document = session.get(MedicalDocument, document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.file_data:
        raise HTTPException(status_code=404, detail="No file data stored")

    return Response(
        content=document.file_data,
        media_type=document.file_type,
        headers={
            "Content-Disposition": f"attachment; filename={document.document_name}"
        }
    )


# -------------------------
# GET ALL DOCUMENTS FOR A PATIENT
# -------------------------
@router.get("/patient/{patient_id}")
def get_patient_documents(
    patient_id: int,
    session: Session = Depends(get_session)
):
    statement = select(MedicalDocument).where(
        MedicalDocument.patient_id == patient_id
    )
    documents = session.exec(statement).all()

    return [
        {
            "document_id": doc.document_id,
            "document_name": doc.document_name,
            "file_type": doc.file_type,
            "uploaded_at": str(doc.uploaded_at) if doc.uploaded_at else None,
            "has_embedding": doc.vector_embedding_id is not None,
            "text_preview": (doc.extracted_text or "")[:200]
        }
        for doc in documents
    ]


# -------------------------
# SEARCH DOCUMENTS (ChromaDB query)
# -------------------------
@router.post("/search")
def search_documents(
    query: str = Form(...),
    patient_id: int = Form(None),
    n_results: int = Form(5)
):
    """Search medical documents using semantic similarity via ChromaDB."""
    results = query_documents(
        query_text=query,
        patient_id=patient_id,
        n_results=n_results
    )

    if not results["documents"] or not results["documents"][0]:
        return {"results": [], "message": "No matching documents found"}

    formatted_results = []
    for i, (doc, meta, dist) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ):
        formatted_results.append({
            "rank": i + 1,
            "document_name": meta.get("document_name", "Unknown"),
            "patient_id": meta.get("patient_id", "Unknown"),
            "similarity_score": round(1 - dist, 4),
            "text_preview": doc[:300] + ("..." if len(doc) > 300 else "")
        })

    return {"results": formatted_results}