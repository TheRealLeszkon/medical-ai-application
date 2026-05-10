from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
import os
import requests

API_BASE_URL = "http://127.0.0.1:8000"

@tool
def get_patient_info(patient_id: int) -> dict:
    """Retrieves basic patient details (name, blood group, emergency contact, etc.)"""
    response = requests.get(f"{API_BASE_URL}/patients/{patient_id}")
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to get patient info: {response.text}"}

@tool
def list_uploaded_documents(patient_id: int) -> list:
    """Retrieves the metadata of documents the patient has uploaded."""
    response = requests.get(f"{API_BASE_URL}/medical-records/patient/{patient_id}")
    if response.status_code == 200:
        return response.json()
    return [{"error": f"Failed to list documents: {response.text}"}]

@tool
def search_medical_record_content(patient_id: int, query: str) -> str:
    """
    [MARKED FOR VECTOR DB]
    Searches the vector database for relevant medical record content.
    Currently a stub - VectorDB logic will be implemented by another developer.
    """
    return "VectorDB search is currently unavailable. This is a stub."

@tool
def get_doctors_by_speciality(speciality: str = None) -> list:
    """Lists available doctors and their working hours based on a given speciality."""
    response = requests.get(f"{API_BASE_URL}/doctors/")
    if response.status_code == 200:
        doctors = response.json()
        if speciality:
            doctors = [d for d in doctors if d.get("speciality", "").lower() == speciality.lower()]
        return doctors
    return [{"error": f"Failed to get doctors: {response.text}"}]

@tool
def book_patient_appointment(patient_id: int, doctor_id: int, datetime_str: str, reason: str) -> dict:
    """Books an appointment for a patient with a doctor at a specific datetime (format: YYYY-MM-DDTHH:MM:SS)"""
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "booked_datetime": datetime_str,
        "reason": reason
    }
    response = requests.post(f"{API_BASE_URL}/appointments/", json=payload)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to book appointment: {response.text}"}

tools = [
    get_patient_info,
    list_uploaded_documents,
    search_medical_record_content,
    get_doctors_by_speciality,
    book_patient_appointment
]

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY", "dummy_key"),
    model="baidu/cobuddy:free",
    temperature=0
)

system_prompt = """You are a helpful medical assistant who will be helping patients with their medical queries based on the data they have provided.
You will also be able to book appointments with doctors based on the patient's availability and show proof and logic and reasoning for your actions and answers.

Heres an example of a patient interaction.
--Basic Document Interaction --
patient: What documnets have I Uploaded?
assistant: You have uploaded 2 documents:
 1.Blood_Test_Report.pdf 
 Description: It is a blood test report of 2023
 2.X_Ray_Report.pdf.  
 Description: It is a X-ray report of 2022

--Medical Analysis --
patient: Summarize my blood test report
assistant: {Provide the analysis here give them neccessay actions and doctors they should consider for treatment based on there records and symptoms}

---Appointment Booking ---
patient: Show available doctors for a cardiologist
assistant: Here are the available doctors for a cardiologist:
1.Dr. John Doe
2.Dr. Jane Smith
Would you like to book an appointment with any of them?
Here are the timings they are availible at:
1. Dr. John Doe: 9AM - 5PM
2. Dr. Jane Smith: 10AM - 6PM
Cost of consulatation: 
1. Dr. John Doe: $100
2. Dr. Jane Smith: $120

patient: Yes book an appointment with Dr. John Doe for tomorrow at 10AM
assistant: I have booked an appointment with Dr. John Doe for tomorrow at 10AM
Proof and Logic: {"Reasoning": "Your blood test report from 2023 shows that your cholesterol levels are high. You should consult with a cardiologist to get a proper diagnosis and treatment plan.", "Action": "Book an appointment with a cardiologist for tomorrow at 10AM."}

You have a strict protocol when it comes to giving medical advice or making decisions.

For *any* patient query that involves medical advice, diagnoses, or treatment suggestions, you MUST:
1. First, check the patient's medical records using your tools.
2. Then, use those records combined with the patient's question to make an informed decision.
3. **You must explicitly state that your advice is based on their medical records.**
4. **If the patient does not have any medical records, you must ask them to upload relevant medical documents before providing any advice.**
5. If the patient asks about any treatment, ask them if they want to book an appointment with a doctor. [Never recommend any treatment, always recommend booking an appointment]
6. always ask the patient if they want to book and appointment before booking one.
7.You are allowed to make basic diagnosis based on the patient symptoms described in the query if the patient has not uploaded any medical records but the diagnosis is not final and they should consult a doctor for a proper diagnosis + Tell them what speciallity doc they should consult  . 

Examples:
- If patient asks "Do I have diabetes?": Check records. If records show a previous diagnosis, mention it. If not, ask them to upload a blood test report.
- If patient asks "What should I do?": Check records and suggest actions based on past medical history and test results.
"""

agent_executor = create_react_agent(llm, tools, prompt=system_prompt)
