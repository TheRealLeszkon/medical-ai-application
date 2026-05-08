from typing import Optional
from datetime import datetime, date

from sqlmodel import SQLModel, Field


class Patient(SQLModel, table=True):
    __tablename__ = "patients"

    patient_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    name: str
    full_legal_name: str

    date_of_birth: date

    blood_group: Optional[str] = None

    government_id_number: str = Field(
        unique=True,
        index=True
    )

    phone_number: str

    emergency_contact: str


class Doctor(SQLModel, table=True):
    __tablename__ = "doctors"

    doctor_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    medical_license_number: str = Field(
        unique=True,
        index=True
    )

    speciality: str

    qualifications: str

    experience_years: int

    workplace_hospital: str

    languages: str

    availability_hours: str

    consultation_fees: float


class MedicalDocument(SQLModel, table=True):
    __tablename__ = "medical_documents"

    document_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    document_name: str

    patient_id: int = Field(
        foreign_key="patients.patient_id",
        index=True
    )

    vector_embedding_id: Optional[str] = None


class Appointment(SQLModel, table=True):
    __tablename__ = "appointments"

    appointment_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    patient_id: int = Field(
        foreign_key="patients.patient_id",
        index=True
    )

    doctor_id: int = Field(
        foreign_key="doctors.doctor_id",
        index=True
    )

    booked_datetime: datetime

    status: str

    paid_fees: float

    reason: Optional[str] = None