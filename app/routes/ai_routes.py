from fastapi import APIRouter

from app.schemas import AIQuestion


router = APIRouter(
    prefix="/ai",
    tags=["AI Agent"]
)


@router.get("/")
def ai_health_check():
    return {
        "status": "Bitch Im Alive!"
    }


@router.post("/answer")
def ai_answer(question: AIQuestion):
    bullshit_response = f"AI response for patient {question.patient_id}: {question.question}"
    return {
        "answer": bullshit_response
    }