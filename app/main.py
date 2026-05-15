from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
import os

from app.database import engine

from app.routes.patient_routes import router as patient_router
from app.routes.doctor_routes import router as doctor_router
from app.routes.medical_record_routes import router as medical_router
from app.routes.ai_routes import router as ai_router
from app.routes.appointment_routes import router as appointment_router


app = FastAPI(
    title="Medical AI Application",
    description="AI-powered medical document management with ChromaDB embeddings and LangChain agent",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# API routes
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(medical_router)
app.include_router(ai_router)
app.include_router(appointment_router)

# Serve static files (frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")