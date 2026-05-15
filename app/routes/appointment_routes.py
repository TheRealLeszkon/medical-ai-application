"""
Appointment routes — browse doctors, get recommendations, and book appointments.
Uses mock data for doctors/hospitals and stores appointments in-memory.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.services.mock_data import (
    MOCK_DOCTORS,
    MOCK_HOSPITALS,
    search_doctors,
    get_doctor_by_id,
    recommend_speciality,
)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

# In-memory appointment store
booked_appointments: list[dict] = []
_appointment_counter = 0


class BookingRequest(BaseModel):
    patient_id: int
    doctor_id: int
    preferred_date: str  # ISO format: "2026-05-20"
    preferred_time: str  # e.g. "10:00 AM"
    reason: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "patient_id": 1,
                "doctor_id": 1,
                "preferred_date": "2026-05-20",
                "preferred_time": "10:00 AM",
                "reason": "Routine cardiac checkup"
            }
        }
    }


# ─── List all doctors ───────────────────────────────────────
@router.get("/doctors")
def list_doctors(speciality: Optional[str] = None, hospital: Optional[str] = None):
    """List all available doctors, optionally filtered by speciality or hospital."""
    results = search_doctors(speciality=speciality, hospital=hospital)
    return {"count": len(results), "doctors": results}


# ─── Get specific doctor ────────────────────────────────────
@router.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    """Get details for a specific doctor."""
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ─── List hospitals ─────────────────────────────────────────
@router.get("/hospitals")
def list_hospitals():
    """List all available hospitals."""
    return {"count": len(MOCK_HOSPITALS), "hospitals": MOCK_HOSPITALS}


# ─── Recommend doctors by symptoms ──────────────────────────
@router.post("/recommend")
def recommend_doctors(symptoms: str):
    """Recommend doctors based on symptoms or condition description."""
    speciality = recommend_speciality(symptoms)
    if not speciality:
        # Fallback to General Medicine
        speciality = "General Medicine"

    doctors = search_doctors(speciality=speciality)
    return {
        "recommended_speciality": speciality,
        "symptoms_analyzed": symptoms,
        "doctors": doctors,
    }


# ─── Book appointment ───────────────────────────────────────
@router.post("/book")
def book_appointment(booking: BookingRequest):
    """Book an appointment with a doctor."""
    global _appointment_counter

    doctor = get_doctor_by_id(booking.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Validate the preferred date is a valid weekday the doctor is available
    try:
        date_obj = datetime.strptime(booking.preferred_date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if day_name not in doctor["availability"]:
        available_days = ", ".join(doctor["availability"].keys())
        raise HTTPException(
            status_code=400,
            detail=f"Dr. {doctor['name'].replace('Dr. ', '')} is not available on {day_name}. "
                   f"Available days: {available_days}",
        )

    _appointment_counter += 1
    appointment = {
        "appointment_id": _appointment_counter,
        "patient_id": booking.patient_id,
        "doctor_id": booking.doctor_id,
        "doctor_name": doctor["name"],
        "speciality": doctor["speciality"],
        "hospital": doctor["hospital"],
        "hospital_address": doctor["hospital_address"],
        "date": booking.preferred_date,
        "day": day_name,
        "time": booking.preferred_time,
        "consultation_fee": doctor["consultation_fee"],
        "reason": booking.reason,
        "status": "confirmed",
        "booked_at": datetime.utcnow().isoformat(),
    }

    booked_appointments.append(appointment)
    return appointment


# ─── List patient appointments ──────────────────────────────
@router.get("/patient/{patient_id}")
def get_patient_appointments(patient_id: int):
    """Get all appointments for a patient."""
    patient_appts = [a for a in booked_appointments if a["patient_id"] == patient_id]
    return {"count": len(patient_appts), "appointments": patient_appts}
