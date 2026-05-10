from fastapi import APIRouter
from app.schemas import AIQuestion
from app.ai.agent import agent_executor

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
    try:
        # Prepend patient_id context to the query so the agent knows who it's talking to
        contextualized_query = f"[System context: My patient ID is {question.patient_id}]\n\n{question.question}"
        
        response = agent_executor.invoke({
            "messages": [("user", contextualized_query)]
        })
        
        # LangGraph agent returns the conversation in "messages", the last one is the AI response
        answer = response["messages"][-1].content
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}