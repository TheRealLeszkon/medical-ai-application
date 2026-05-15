"""
LangChain agent with multiple tools for medical document Q&A
and appointment booking.

Tools:
  1. search_medical_records - Search ChromaDB for relevant documents
  2. get_patient_info - Get patient details from PostgreSQL
  3. list_patient_documents - List all documents for a patient
  4. search_doctors - Search/filter available doctors
  5. recommend_doctor - Recommend doctors based on symptoms
  6. book_appointment - Book an appointment with a doctor
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from sqlmodel import Session

from app.database import engine
from app.models import Patient, MedicalDocument
from app.services.chromadb_service import query_documents, get_all_documents_for_patient
from app.services.mock_data import (
    search_doctors as _search_doctors,
    get_doctor_by_id,
    recommend_speciality,
    MOCK_DOCTORS,
)
from app.routes.appointment_routes import booked_appointments, _appointment_counter

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
    max_tokens=1024,
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
# TOOL 4: Search Doctors
# ========================================
@tool
def search_doctors(speciality: str = "", hospital: str = "") -> str:
    """
    Search for available doctors. Can filter by speciality and/or hospital.
    Use this tool when the user asks to see available doctors, or asks about
    a specific speciality or hospital.
    
    Args:
        speciality: Optional speciality to filter by (e.g. "Cardiology", "Neurology")
        hospital: Optional hospital name to filter by (e.g. "Apollo")
    
    Returns:
        List of matching doctors with details
    """
    results = _search_doctors(
        speciality=speciality if speciality else None,
        hospital=hospital if hospital else None,
    )

    if not results:
        return "No doctors found matching your criteria."

    lines = [f"Found {len(results)} doctor(s):\n"]
    for doc in results:
        avail = ", ".join([f"{day}: {hours}" for day, hours in doc["availability"].items()])
        lines.append(
            f"• **{doc['name']}** (ID: {doc['doctor_id']})\n"
            f"  Speciality: {doc['speciality']}\n"
            f"  Hospital: {doc['hospital']}\n"
            f"  Experience: {doc['experience_years']} years\n"
            f"  Fee: ₹{doc['consultation_fee']}\n"
            f"  Rating: {doc['rating']}★\n"
            f"  Availability: {avail}\n"
        )

    return "\n".join(lines)


# ========================================
# TOOL 5: Recommend Doctor
# ========================================
@tool
def recommend_doctor(symptoms: str) -> str:
    """
    Recommend a doctor based on the patient's symptoms or health concern.
    Use this tool when a user describes symptoms and wants to know which 
    type of doctor to see.
    
    Args:
        symptoms: Description of the patient's symptoms or health concern
    
    Returns:
        Recommended speciality and matching doctors
    """
    speciality = recommend_speciality(symptoms)
    if not speciality:
        speciality = "General Medicine"

    doctors = _search_doctors(speciality=speciality)

    if not doctors:
        return f"Based on your symptoms, I recommend seeing a {speciality} specialist, but no matching doctors are available in our system."

    lines = [
        f"Based on your symptoms (\"{symptoms}\"), I recommend seeing a **{speciality}** specialist.\n",
        f"Available {speciality} doctors:\n"
    ]
    for doc in doctors:
        lines.append(
            f"• **{doc['name']}** (ID: {doc['doctor_id']}) — "
            f"{doc['hospital']}, "
            f"₹{doc['consultation_fee']}, "
            f"{doc['rating']}★, "
            f"{doc['experience_years']}y exp"
        )

    lines.append(
        f"\nTo book, tell me the doctor ID, your preferred date and time."
    )

    return "\n".join(lines)


# ========================================
# TOOL 6: Book Appointment
# ========================================
@tool
def book_appointment(patient_id: int, doctor_id: int, preferred_date: str, preferred_time: str, reason: str = "") -> str:
    """
    Book an appointment with a doctor for a patient.
    Use this tool when the user confirms they want to book an appointment.
    
    Args:
        patient_id: The patient ID booking the appointment
        doctor_id: The doctor ID to book with
        preferred_date: Date in YYYY-MM-DD format (e.g. "2026-05-20")
        preferred_time: Time slot (e.g. "10:00 AM")
        reason: Optional reason for the visit
    
    Returns:
        Appointment confirmation with details
    """
    import app.routes.appointment_routes as appt_module

    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        return f"Doctor with ID {doctor_id} not found. Please provide a valid doctor ID."

    # Validate date
    try:
        date_obj = datetime.strptime(preferred_date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format (e.g., 2026-05-20)."

    # Check if past
    if date_obj.date() < datetime.now().date():
        return "Cannot book appointments in the past. Please choose a future date."

    # Check availability
    if day_name not in doctor["availability"]:
        available_days = ", ".join(doctor["availability"].keys())
        return (
            f"{doctor['name']} is not available on {day_name}s. "
            f"Available days: {available_days}. "
            f"Please choose a different date."
        )

    # Create the appointment
    appt_module._appointment_counter += 1
    appointment = {
        "appointment_id": appt_module._appointment_counter,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "doctor_name": doctor["name"],
        "speciality": doctor["speciality"],
        "hospital": doctor["hospital"],
        "hospital_address": doctor["hospital_address"],
        "date": preferred_date,
        "day": day_name,
        "time": preferred_time,
        "consultation_fee": doctor["consultation_fee"],
        "reason": reason,
        "status": "confirmed",
        "booked_at": datetime.utcnow().isoformat(),
    }
    appt_module.booked_appointments.append(appointment)

    return (
        f"✅ APPOINTMENT CONFIRMED!\n\n"
        f"📋 Appointment ID: #{appointment['appointment_id']}\n"
        f"👨‍⚕️ Doctor: {doctor['name']} ({doctor['speciality']})\n"
        f"🏥 Hospital: {doctor['hospital']}\n"
        f"📍 Address: {doctor['hospital_address']}\n"
        f"📅 Date: {preferred_date} ({day_name})\n"
        f"🕐 Time: {preferred_time}\n"
        f"💰 Consultation Fee: ₹{doctor['consultation_fee']}\n"
        f"📝 Reason: {reason or 'General consultation'}\n\n"
        f"Doctor's hours on {day_name}: {doctor['availability'][day_name]}\n"
        f"Please arrive 15 minutes early with your ID and medical records."
    )


# ========================================
# Build the LangChain Agent
# ========================================
tools = [
    search_medical_records,
    get_patient_info,
    list_patient_documents,
    search_doctors,
    recommend_doctor,
    book_appointment,
]

SYSTEM_PROMPT = (
    "You are a medical AI assistant called MediVault AI. You help patients with their "
    "medical records AND appointment booking.\n\n"
    "CAPABILITIES:\n"
    "- Search and analyze medical records\n"
    "- Get patient information\n"
    "- List patient documents\n"
    "- Search for doctors by speciality or hospital\n"
    "- Recommend doctors based on symptoms\n"
    "- Book appointments with doctors\n\n"
    "APPOINTMENT BOOKING RULES:\n"
    "- When a user describes symptoms, use recommend_doctor to suggest specialists\n"
    "- Present doctor options clearly with their ID, name, hospital, fee, and rating\n"
    "- When the user picks a doctor, ask for their preferred date and time if not provided\n"
    "- Use book_appointment to finalize the booking\n"
    "- After booking, always relay the full confirmation including time and location\n\n"
    "GENERAL RULES:\n"
    "- Give clear, well-formatted answers\n"
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


# ========================================
# Conversation History (per-patient)
# ========================================
# Stores message history keyed by patient_id so the agent
# can reference prior turns (e.g. "book that doctor" after
# a recommendation).  Capped at MAX_HISTORY_TURNS to prevent
# token overflow.
MAX_HISTORY_TURNS = 20  # each turn = 1 human + 1 AI message

from langchain_core.messages import AIMessage

conversation_histories: dict[int, list] = {}


def clear_history(patient_id: int) -> None:
    """Clear conversation history for a specific patient."""
    conversation_histories.pop(patient_id, None)


def clear_all_history() -> None:
    """Clear all conversation histories."""
    conversation_histories.clear()


def get_history(patient_id: int) -> list[dict]:
    """Get the conversation history for a patient in a UI-friendly format."""
    history = conversation_histories.get(patient_id, [])
    formatted_history = []
    
    for msg in history:
        role = "ai" if isinstance(msg, AIMessage) else "user"
        content = msg.content
        
        # Strip the "Patient ID: X\nQuestion: " prefix from user messages for UI display
        if role == "user" and content.startswith("Patient ID:"):
            try:
                content = content.split("Question: ", 1)[1]
            except IndexError:
                pass
                
        formatted_history.append({
            "role": role,
            "content": content
        })
        
    return formatted_history


async def run_agent(patient_id: int, question: str) -> str:
    """
    Run the LangChain agent to answer a medical question.
    Maintains per-patient conversation history so the AI is
    aware of the full chat context.
    
    Args:
        patient_id: The patient ID for context
        question: The user's question
    
    Returns:
        The agent's response as a string
    """
    # Build the new user message
    user_message = (
        f"Patient ID: {patient_id}\n"
        f"Question: {question}"
    )

    # Retrieve or initialize conversation history for this patient
    if patient_id not in conversation_histories:
        conversation_histories[patient_id] = []

    history = conversation_histories[patient_id]

    # Build the full message list: history + new message
    messages = list(history) + [HumanMessage(content=user_message)]

    try:
        result = await agent.ainvoke({"messages": messages})

        # Extract only the final AIMessage (not ToolMessages or HumanMessages)
        final_response = None
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
                final_response = msg.content
                break

        if final_response:
            # Save this turn to history (human + AI only, skip tool messages)
            history.append(HumanMessage(content=user_message))
            history.append(AIMessage(content=final_response))

            # Trim to MAX_HISTORY_TURNS (each turn = 2 messages)
            max_messages = MAX_HISTORY_TURNS * 2
            if len(history) > max_messages:
                conversation_histories[patient_id] = history[-max_messages:]

            return final_response

        return "I couldn't generate a response. Please try rephrasing your question."

    except Exception as e:
        return f"An error occurred while processing your question: {str(e)}"
