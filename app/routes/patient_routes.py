from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Patient
from app.schemas import PatientCreate, PatientUpdate


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# -------------------------
# GET PATIENT
# -------------------------

@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    session: Session = Depends(get_session)
):
    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# -------------------------
# REGISTER PATIENT
# -------------------------

@router.post("/")
def register_patient(
    patient_data: PatientCreate,
    session: Session = Depends(get_session)
):
    patient = Patient.model_validate(patient_data)

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


# -------------------------
# UPDATE PATIENT
# -------------------------

@router.patch("/{patient_id}")
def update_patient(
    patient_id: int,
    update_data: PatientUpdate,
    session: Session = Depends(get_session)
):
    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(patient, key, value)

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient