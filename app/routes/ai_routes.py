"""
AI routes - handles Q&A using LangChain agent with multiple tools.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas import AIQuestion
from app.services.langchain_agent import run_agent


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
            "list_patient_documents"
        ]
    }


@router.post("/ask")
async def ai_ask(question: AIQuestion):
    """
    Ask the AI agent a question about a patient's medical records.
    The agent uses LangChain with multiple tools:
    - search_medical_records: Searches ChromaDB for relevant documents
    - get_patient_info: Gets patient details from PostgreSQL
    - list_patient_documents: Lists all stored documents
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