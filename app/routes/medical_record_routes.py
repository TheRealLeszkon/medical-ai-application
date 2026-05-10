from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select

from app.database import get_session
from app.models import MedicalDocument, Patient
from app.schemas import MedicalDocumentRead

router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"]
)

@router.get("/patient/{patient_id}", response_model=list[MedicalDocumentRead])
def get_patient_documents(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    docs = session.exec(select(MedicalDocument).where(MedicalDocument.patient_id == patient_id)).all()
    return docs

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
async def upload_medical_record(
    patient_id: int = Form(...),
    vector_embedding_id: str | None = Form(None),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    file_bytes = await file.read()
    
    document = MedicalDocument(
        document_name=file.filename,
        file_data=file_bytes,
        mime_type=file.content_type,
        patient_id=patient_id,
        vector_embedding_id=vector_embedding_id
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    return {
        "message": "Medical record uploaded successfully.",
        "document_id": document.document_id,
        "document_name": document.document_name
    }

# @router.put("/{document_id}")
# def update_document(
#     document_id: int,
#     record_data: MedicalRecordCreate,
#     session: Session = Depends(get_session)
# ):
#     document = session.get(MedicalDocument, document_id)

#     if not document:
#         raise HTTPException(
#             status_code=404,
#             detail="Document not found"
#         )

#     update_dict = record_data.model_dump()

#     for key, value in update_dict.items():
#         setattr(document, key, value)

#     session.commit()
#     session.refresh(document)

#     return document