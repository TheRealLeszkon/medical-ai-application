from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Appointment, Patient, Doctor
from app.schemas import AppointmentCreate, AppointmentRead

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

@router.post("/", response_model=AppointmentRead)
def book_appointment(
    appointment_data: AppointmentCreate,
    session: Session = Depends(get_session)
):
    patient = session.get(Patient, appointment_data.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    doctor = session.get(Doctor, appointment_data.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    # Check if there is another appointment at the exact same time
    overlapping_appointment = session.exec(
        select(Appointment).where(
            Appointment.doctor_id == appointment_data.doctor_id,
            Appointment.booked_datetime == appointment_data.booked_datetime
        )
    ).first()
    
    if overlapping_appointment:
        raise HTTPException(status_code=400, detail="Doctor is already booked at this time.")
        
    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        booked_datetime=appointment_data.booked_datetime,
        reason=appointment_data.reason,
        status="Scheduled",
        paid_fees=0.0
    )
    
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    
    return appointment

@router.get("/doctor/{doctor_id}", response_model=list[AppointmentRead])
def get_doctor_appointments(doctor_id: int, session: Session = Depends(get_session)):
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    appointments = session.exec(
        select(Appointment).where(Appointment.doctor_id == doctor_id)
    ).all()
    
    return appointments

@router.get("/patient/{patient_id}", response_model=list[AppointmentRead])
def get_patient_appointments(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    appointments = session.exec(
        select(Appointment).where(Appointment.patient_id == patient_id)
    ).all()
    
    return appointments
