from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Doctor
from app.schemas import DoctorCreate, DoctorUpdate


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)

@router.get("/")
def list_doctors(session: Session = Depends(get_session)):
    doctors = session.exec(select(Doctor)).all()
    return doctors


@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    session: Session = Depends(get_session)
):
    doctor = session.get(Doctor, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.post("/")
def register_doctor(
    doctor_data: DoctorCreate,
    session: Session = Depends(get_session)
):
    doctor = Doctor.model_validate(doctor_data)

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return doctor


@router.patch("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    update_data: DoctorUpdate,
    session: Session = Depends(get_session)
):
    doctor = session.get(Doctor, doctor_id)

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(doctor, key, value)

    session.commit()
    session.refresh(doctor)

    return doctor