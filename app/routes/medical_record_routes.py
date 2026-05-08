from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.models import MedicalDocument
from app.schemas import MedicalRecordCreate


router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"]
)


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

    return document


@router.post("/")
def upload_medical_record(
    record_data: MedicalRecordCreate,
    session: Session = Depends(get_session)
):
    document = MedicalDocument.model_validate(record_data)

    session.add(document)
    session.commit()
    session.refresh(document)

    return {
        "message": (
            "Medical record stored successfully. "
            "Patient can upload documents later."
        ),
        "document": document
    }


@router.put("/{document_id}")
def update_document(
    document_id: int,
    record_data: MedicalRecordCreate,
    session: Session = Depends(get_session)
):
    document = session.get(MedicalDocument, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    update_dict = record_data.model_dump()

    for key, value in update_dict.items():
        setattr(document, key, value)

    session.commit()
    session.refresh(document)

    return document