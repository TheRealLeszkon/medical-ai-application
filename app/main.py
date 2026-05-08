from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine

from app.routes.patient_routes import router as patient_router
from app.routes.doctor_routes import router as doctor_router
from app.routes.medical_record_routes import router as medical_router
from app.routes.ai_routes import router as ai_router


app = FastAPI(
    title="Medical AI Application"
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(medical_router)
app.include_router(ai_router)