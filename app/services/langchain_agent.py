"""
LangChain agent with multiple tools for medical document Q&A.
Tools:
  1. search_medical_records - Search ChromaDB for relevant documents
  2. get_patient_info - Get patient details from PostgreSQL
  3. list_patient_documents - List all documents for a patient
"""

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from sqlmodel import Session

from app.database import engine
from app.models import Patient, MedicalDocument
from app.services.chromadb_service import query_documents, get_all_documents_for_patient

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")


# Initialize the LLM via OpenRouter (OpenAI-compatible API)
llm = ChatOpenAI(
    model="poolside/laguna-xs.2:free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Medical AI Application"
    },
    temperature=0.3,
    max_tokens=512,
)


# ========================================
# TOOL 1: Search Medical Records in ChromaDB
# ========================================
@tool
def search_medical_records(query: str, patient_id: int) -> str:
    """
    Search through a patient's medical records to find relevant information.
    Use this tool when you need to find specific medical information from stored documents.
    
    Args:
        query: The search query describing what information to look for
        patient_id: The patient ID to search records for
    
    Returns:
        Relevant medical document excerpts
    """
    results = query_documents(query_text=query, patient_id=patient_id, n_results=5)

    if not results["documents"] or not results["documents"][0]:
        return f"No medical records found for patient {patient_id}."

    output_parts = []
    for i, (doc, meta) in enumerate(
        zip(results["documents"][0], results["metadatas"][0])
    ):
        # Truncate each doc to 500 chars to save tokens
        snippet = doc[:500] + ("..." if len(doc) > 500 else "")
        output_parts.append(
            f"[{meta.get('document_name', 'Unknown')}]: {snippet}"
        )

    return "\n".join(output_parts)


# ========================================
# TOOL 2: Get Patient Info from PostgreSQL
# ========================================
@tool
def get_patient_info(patient_id: int) -> str:
    """
    Get patient demographic and contact information from the database.
    Use this tool when you need patient details like name, date of birth, blood group, etc.
    
    Args:
        patient_id: The patient ID to look up
    
    Returns:
        Patient information as a formatted string
    """
    with Session(engine) as session:
        patient = session.get(Patient, patient_id)

    if not patient:
        return f"Patient with ID {patient_id} not found."

    return (
        f"Patient ID: {patient.patient_id}\n"
        f"Name: {patient.name}\n"
        f"Full Legal Name: {patient.full_legal_name}\n"
        f"Date of Birth: {patient.date_of_birth}\n"
        f"Blood Group: {patient.blood_group or 'Not recorded'}\n"
        f"Phone: {patient.phone_number}\n"
        f"Emergency Contact: {patient.emergency_contact}"
    )


# ========================================
# TOOL 3: List Patient Documents
# ========================================
@tool
def list_patient_documents(patient_id: int) -> str:
    """
    List all medical documents stored for a patient.
    Use this tool to see what documents are available before searching.
    
    Args:
        patient_id: The patient ID to list documents for
    
    Returns:
        List of document names and IDs
    """
    with Session(engine) as session:
        from sqlmodel import select
        statement = select(MedicalDocument).where(
            MedicalDocument.patient_id == patient_id
        )
        documents = session.exec(statement).all()

    if not documents:
        return f"No documents found for patient {patient_id}."

    lines = [f"Documents for Patient {patient_id}:"]
    for doc in documents:
        lines.append(
            f"  - ID: {doc.document_id} | Name: {doc.document_name} | "
            f"Embedding: {'Yes' if doc.vector_embedding_id else 'No'}"
        )

    return "\n".join(lines)


# ========================================
# Build the LangChain Agent
# ========================================
tools = [search_medical_records, get_patient_info, list_patient_documents]

SYSTEM_PROMPT = (
    "You are a medical AI assistant. You have tools to search patient records, "
    "get patient info, and list documents.\n\n"
    "RULES:\n"
    "- Give SHORT, DIRECT answers (2-4 sentences max)\n"
    "- Do NOT repeat or dump raw document text back to the user\n"
    "- Extract only the specific info the user asked about\n"
    "- If not found, say so in one sentence\n"
    "- Never fabricate medical data\n"
    "- End with a brief disclaimer if giving health-related info"
)

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
)


async def run_agent(patient_id: int, question: str) -> str:
    """
    Run the LangChain agent to answer a medical question.
    
    Args:
        patient_id: The patient ID for context
        question: The user's question
    
    Returns:
        The agent's response as a string
    """
    user_message = (
        f"Patient ID: {patient_id}\n"
        f"Question: {question}"
    )

    try:
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=user_message)]}
        )

        # Extract only the final AIMessage (not ToolMessages or HumanMessages)
        from langchain_core.messages import AIMessage
        final_response = None
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
                final_response = msg.content
                break

        if final_response:
            return final_response

        return "I couldn't generate a response. Please try rephrasing your question."

    except Exception as e:
        return f"An error occurred while processing your question: {str(e)}"
