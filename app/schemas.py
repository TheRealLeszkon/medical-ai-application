from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel



class PatientCreate(BaseModel):
    name: str
    full_legal_name: str
    date_of_birth: date
    blood_group: Optional[str] = None
    government_id_number: str
    phone_number: str
    emergency_contact: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Kevin",
                "full_legal_name": "Michael Kevin",
                "date_of_birth": "2003-04-12",
                "blood_group": "O+",
                "government_id_number": "123456789012",
                "phone_number": "9876543210",
                "emergency_contact": "9123456780"
            }
        }
    }


class PatientUpdate(BaseModel):
    phone_number: Optional[str] = None
    emergency_contact: Optional[str] = None
    blood_group: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "phone_number": "9999999999",
                "emergency_contact": "9123456780",
                "blood_group": "A+"
            }
        }
    }


class DoctorCreate(BaseModel):
    medical_license_number: str
    speciality: str
    qualifications: str
    experience_years: int
    workplace_hospital: str
    languages: str
    availability_hours: str
    consultation_fees: float
    model_config = {
        "json_schema_extra": {
            "example": {
                "medical_license_number": "TNMC123456",
                "speciality": "Cardiology",
                "qualifications": "MBBS, MD Cardiology",
                "experience_years": 12,
                "workplace_hospital": "Apollo Hospital Chennai",
                "languages": "English, Tamil",
                "availability_hours": "9AM - 5PM",
                "consultation_fees": 1200
            }
        }
    }


class DoctorUpdate(BaseModel):
    availability_hours: Optional[str] = None
    consultation_fees: Optional[float] = None


class MedicalRecordCreate(BaseModel):
    document_name: str
    patient_id: int
    vector_embedding_id: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "document_name": "Blood_Test_Report.pdf",
                "patient_id": 1,
                "doctor_id": 1,
                "vector_embedding_id": "chroma://embedding/abc123"
            }
        }
    }


class AIQuestion(BaseModel):
    patient_id: int
    question: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "patient_id": 1,
                "question": "Summarize my recent blood report"
            }
        }
    }


class MedicalDocumentRead(BaseModel):
    document_id: int
    document_name: str
    mime_type: str
    patient_id: int
    vector_embedding_id: Optional[str] = None
    uploaded_at: datetime
    model_config = {
        "json_schema_extra": {
            "example": {
                "document_id": 1,
                "document_name": "Blood_Test_Report.pdf",
                "mime_type": "application/pdf",
                "patient_id": 1,
                "vector_embedding_id": "abc12345",
                "uploaded_at": "2026-05-10T10:30:00"
            }
        }
    }


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    booked_datetime: datetime
    reason: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "patient_id": 1,
                "doctor_id": 2,
                "booked_datetime": "2026-05-15T10:30:00",
                "reason": "Routine Checkup"
            }
        }
    }


class AppointmentRead(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    booked_datetime: datetime
    status: str
    paid_fees: float
    reason: Optional[str] = None