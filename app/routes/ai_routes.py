"""
AI routes - handles Q&A using LangChain agent with multiple tools.
Maintains per-patient conversation history for contextual awareness.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas import AIQuestion
from app.services.langchain_agent import run_agent, clear_history, clear_all_history, get_history


router = APIRouter(
    prefix="/ai",
    tags=["AI Agent"]
)


@router.get("/")
def ai_health_check():
    return {
        "status": "AI Agent is ready!",
        "tools": [
            "search_medical_records",
            "get_patient_info",
            "list_patient_documents",
            "search_doctors",
            "recommend_doctor",
            "book_appointment",
        ]
    }


@router.post("/ask")
async def ai_ask(question: AIQuestion):
    """
    Ask the AI agent a question about a patient's medical records.
    The agent maintains conversation history per patient so it can
    reference prior messages (e.g. "book that doctor" after a recommendation).
    """
    answer = await run_agent(
        patient_id=question.patient_id,
        question=question.question
    )

    return {
        "patient_id": question.patient_id,
        "question": question.question,
        "answer": answer
    }


@router.delete("/history/{patient_id}")
def delete_patient_history(patient_id: int):
    """
    Clear conversation history for a specific patient.
    Called when the user switches patient context or wants a fresh start.
    """
    clear_history(patient_id)
    return {"status": "ok", "message": f"Conversation history cleared for patient {patient_id}"}


@router.get("/history/{patient_id}")
def get_patient_history(patient_id: int):
    """
    Get conversation history for a specific patient.
    """
    history = get_history(patient_id)
    return {"history": history}


@router.delete("/history")
def delete_all_history():
    """Clear all conversation histories."""
    clear_all_history()
    return {"status": "ok", "message": "All conversation histories cleared"}