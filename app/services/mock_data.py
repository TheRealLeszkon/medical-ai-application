"""
Mock data for hospitals, doctors, and their specializations.
Used by the appointment booking tool for doctor recommendations.
"""

MOCK_DOCTORS = [
    {
        "doctor_id": 1,
        "name": "Dr. Priya Sharma",
        "speciality": "Cardiology",
        "qualifications": "MBBS, MD Cardiology, DM Interventional Cardiology",
        "experience_years": 18,
        "hospital": "Apollo Hospital, Chennai",
        "hospital_address": "21, Greams Lane, Off Greams Road, Chennai - 600006",
        "languages": "English, Tamil, Hindi",
        "availability": {
            "Monday": "9:00 AM - 1:00 PM",
            "Tuesday": "9:00 AM - 1:00 PM",
            "Wednesday": "2:00 PM - 6:00 PM",
            "Thursday": "9:00 AM - 1:00 PM",
            "Friday": "9:00 AM - 1:00 PM",
            "Saturday": "10:00 AM - 12:00 PM",
        },
        "consultation_fee": 1200,
        "rating": 4.8,
    },
    {
        "doctor_id": 2,
        "name": "Dr. Rajesh Kumar",
        "speciality": "Neurology",
        "qualifications": "MBBS, MD Internal Medicine, DM Neurology",
        "experience_years": 15,
        "hospital": "Fortis Malar Hospital, Chennai",
        "hospital_address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai - 600020",
        "languages": "English, Tamil",
        "availability": {
            "Monday": "10:00 AM - 2:00 PM",
            "Tuesday": "10:00 AM - 2:00 PM",
            "Wednesday": "10:00 AM - 2:00 PM",
            "Thursday": "3:00 PM - 7:00 PM",
            "Friday": "10:00 AM - 2:00 PM",
        },
        "consultation_fee": 1500,
        "rating": 4.7,
    },
    {
        "doctor_id": 3,
        "name": "Dr. Aishwarya Nair",
        "speciality": "Dermatology",
        "qualifications": "MBBS, MD Dermatology",
        "experience_years": 10,
        "hospital": "MIOT International, Chennai",
        "hospital_address": "4/112, Mount Poonamallee Road, Manapakkam, Chennai - 600089",
        "languages": "English, Tamil, Malayalam",
        "availability": {
            "Monday": "11:00 AM - 4:00 PM",
            "Tuesday": "11:00 AM - 4:00 PM",
            "Wednesday": "11:00 AM - 4:00 PM",
            "Thursday": "11:00 AM - 4:00 PM",
            "Friday": "11:00 AM - 4:00 PM",
            "Saturday": "9:00 AM - 1:00 PM",
        },
        "consultation_fee": 800,
        "rating": 4.6,
    },
    {
        "doctor_id": 4,
        "name": "Dr. Vikram Patel",
        "speciality": "Orthopedics",
        "qualifications": "MBBS, MS Orthopedics, Fellowship in Joint Replacement",
        "experience_years": 22,
        "hospital": "Apollo Hospital, Chennai",
        "hospital_address": "21, Greams Lane, Off Greams Road, Chennai - 600006",
        "languages": "English, Hindi, Gujarati",
        "availability": {
            "Monday": "8:00 AM - 12:00 PM",
            "Tuesday": "2:00 PM - 6:00 PM",
            "Wednesday": "8:00 AM - 12:00 PM",
            "Thursday": "2:00 PM - 6:00 PM",
            "Friday": "8:00 AM - 12:00 PM",
            "Saturday": "9:00 AM - 11:00 AM",
        },
        "consultation_fee": 1400,
        "rating": 4.9,
    },
    {
        "doctor_id": 5,
        "name": "Dr. Meena Sundaram",
        "speciality": "Gynecology",
        "qualifications": "MBBS, MD Obstetrics & Gynecology",
        "experience_years": 14,
        "hospital": "Kauvery Hospital, Chennai",
        "hospital_address": "199, Luz Church Road, Mylapore, Chennai - 600004",
        "languages": "English, Tamil",
        "availability": {
            "Monday": "9:00 AM - 1:00 PM",
            "Tuesday": "9:00 AM - 1:00 PM",
            "Wednesday": "9:00 AM - 1:00 PM",
            "Thursday": "3:00 PM - 7:00 PM",
            "Friday": "9:00 AM - 1:00 PM",
            "Saturday": "10:00 AM - 12:00 PM",
        },
        "consultation_fee": 1000,
        "rating": 4.7,
    },
    {
        "doctor_id": 6,
        "name": "Dr. Arjun Reddy",
        "speciality": "General Medicine",
        "qualifications": "MBBS, MD General Medicine",
        "experience_years": 12,
        "hospital": "Fortis Malar Hospital, Chennai",
        "hospital_address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai - 600020",
        "languages": "English, Tamil, Telugu",
        "availability": {
            "Monday": "8:00 AM - 2:00 PM",
            "Tuesday": "8:00 AM - 2:00 PM",
            "Wednesday": "8:00 AM - 2:00 PM",
            "Thursday": "8:00 AM - 2:00 PM",
            "Friday": "8:00 AM - 2:00 PM",
            "Saturday": "9:00 AM - 12:00 PM",
        },
        "consultation_fee": 600,
        "rating": 4.5,
    },
    {
        "doctor_id": 7,
        "name": "Dr. Lakshmi Venkatesh",
        "speciality": "Pediatrics",
        "qualifications": "MBBS, MD Pediatrics, Fellowship in Neonatology",
        "experience_years": 16,
        "hospital": "MIOT International, Chennai",
        "hospital_address": "4/112, Mount Poonamallee Road, Manapakkam, Chennai - 600089",
        "languages": "English, Tamil, Kannada",
        "availability": {
            "Monday": "9:00 AM - 3:00 PM",
            "Tuesday": "9:00 AM - 3:00 PM",
            "Wednesday": "9:00 AM - 12:00 PM",
            "Thursday": "9:00 AM - 3:00 PM",
            "Friday": "9:00 AM - 3:00 PM",
        },
        "consultation_fee": 900,
        "rating": 4.8,
    },
    {
        "doctor_id": 8,
        "name": "Dr. Sanjay Gupta",
        "speciality": "Pulmonology",
        "qualifications": "MBBS, MD Pulmonary Medicine, DM Pulmonology",
        "experience_years": 20,
        "hospital": "Kauvery Hospital, Chennai",
        "hospital_address": "199, Luz Church Road, Mylapore, Chennai - 600004",
        "languages": "English, Hindi, Tamil",
        "availability": {
            "Monday": "10:00 AM - 2:00 PM",
            "Tuesday": "10:00 AM - 2:00 PM",
            "Wednesday": "3:00 PM - 7:00 PM",
            "Thursday": "10:00 AM - 2:00 PM",
            "Friday": "10:00 AM - 2:00 PM",
        },
        "consultation_fee": 1100,
        "rating": 4.6,
    },
    {
        "doctor_id": 9,
        "name": "Dr. Kavitha Rajan",
        "speciality": "Ophthalmology",
        "qualifications": "MBBS, MS Ophthalmology, Fellowship in Retina",
        "experience_years": 11,
        "hospital": "Apollo Hospital, Chennai",
        "hospital_address": "21, Greams Lane, Off Greams Road, Chennai - 600006",
        "languages": "English, Tamil",
        "availability": {
            "Monday": "9:00 AM - 1:00 PM",
            "Tuesday": "2:00 PM - 6:00 PM",
            "Wednesday": "9:00 AM - 1:00 PM",
            "Thursday": "9:00 AM - 1:00 PM",
            "Friday": "2:00 PM - 6:00 PM",
            "Saturday": "9:00 AM - 12:00 PM",
        },
        "consultation_fee": 950,
        "rating": 4.7,
    },
    {
        "doctor_id": 10,
        "name": "Dr. Mohammed Farooq",
        "speciality": "ENT",
        "qualifications": "MBBS, MS ENT, Fellowship in Head & Neck Surgery",
        "experience_years": 13,
        "hospital": "Fortis Malar Hospital, Chennai",
        "hospital_address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai - 600020",
        "languages": "English, Tamil, Urdu",
        "availability": {
            "Monday": "10:00 AM - 3:00 PM",
            "Tuesday": "10:00 AM - 3:00 PM",
            "Wednesday": "10:00 AM - 3:00 PM",
            "Thursday": "10:00 AM - 3:00 PM",
            "Friday": "10:00 AM - 12:00 PM",
        },
        "consultation_fee": 850,
        "rating": 4.5,
    },
    {
        "doctor_id": 11,
        "name": "Dr. Deepa Krishnan",
        "speciality": "Psychiatry",
        "qualifications": "MBBS, MD Psychiatry",
        "experience_years": 9,
        "hospital": "Kauvery Hospital, Chennai",
        "hospital_address": "199, Luz Church Road, Mylapore, Chennai - 600004",
        "languages": "English, Tamil, Hindi",
        "availability": {
            "Monday": "11:00 AM - 5:00 PM",
            "Tuesday": "11:00 AM - 5:00 PM",
            "Wednesday": "11:00 AM - 5:00 PM",
            "Thursday": "11:00 AM - 5:00 PM",
            "Friday": "11:00 AM - 3:00 PM",
        },
        "consultation_fee": 1300,
        "rating": 4.8,
    },
    {
        "doctor_id": 12,
        "name": "Dr. Suresh Babu",
        "speciality": "Gastroenterology",
        "qualifications": "MBBS, MD Internal Medicine, DM Gastroenterology",
        "experience_years": 17,
        "hospital": "MIOT International, Chennai",
        "hospital_address": "4/112, Mount Poonamallee Road, Manapakkam, Chennai - 600089",
        "languages": "English, Tamil, Telugu",
        "availability": {
            "Monday": "9:00 AM - 1:00 PM",
            "Tuesday": "9:00 AM - 1:00 PM",
            "Wednesday": "2:00 PM - 6:00 PM",
            "Thursday": "9:00 AM - 1:00 PM",
            "Friday": "9:00 AM - 1:00 PM",
            "Saturday": "10:00 AM - 12:00 PM",
        },
        "consultation_fee": 1200,
        "rating": 4.6,
    },
]

# Unique hospitals derived from the doctors data
MOCK_HOSPITALS = [
    {
        "name": "Apollo Hospital, Chennai",
        "address": "21, Greams Lane, Off Greams Road, Chennai - 600006",
        "phone": "044-2829 3333",
        "specialities": ["Cardiology", "Orthopedics", "Ophthalmology"],
    },
    {
        "name": "Fortis Malar Hospital, Chennai",
        "address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai - 600020",
        "phone": "044-4289 2222",
        "specialities": ["Neurology", "General Medicine", "ENT"],
    },
    {
        "name": "MIOT International, Chennai",
        "address": "4/112, Mount Poonamallee Road, Manapakkam, Chennai - 600089",
        "phone": "044-4200 0000",
        "specialities": ["Dermatology", "Pediatrics", "Gastroenterology"],
    },
    {
        "name": "Kauvery Hospital, Chennai",
        "address": "199, Luz Church Road, Mylapore, Chennai - 600004",
        "phone": "044-4000 6000",
        "specialities": ["Gynecology", "Pulmonology", "Psychiatry"],
    },
]

# Symptom-to-speciality mapping for AI recommendations
SYMPTOM_SPECIALITY_MAP = {
    # Cardiology
    "chest pain": "Cardiology",
    "heart": "Cardiology",
    "palpitation": "Cardiology",
    "blood pressure": "Cardiology",
    "hypertension": "Cardiology",
    "cardiac": "Cardiology",
    # Neurology
    "headache": "Neurology",
    "migraine": "Neurology",
    "seizure": "Neurology",
    "numbness": "Neurology",
    "dizziness": "Neurology",
    "nerve": "Neurology",
    "brain": "Neurology",
    "stroke": "Neurology",
    # Dermatology
    "skin": "Dermatology",
    "rash": "Dermatology",
    "acne": "Dermatology",
    "eczema": "Dermatology",
    "allergy": "Dermatology",
    "itch": "Dermatology",
    # Orthopedics
    "bone": "Orthopedics",
    "joint": "Orthopedics",
    "fracture": "Orthopedics",
    "back pain": "Orthopedics",
    "knee": "Orthopedics",
    "spine": "Orthopedics",
    "arthritis": "Orthopedics",
    # Gynecology
    "pregnancy": "Gynecology",
    "menstrual": "Gynecology",
    "period": "Gynecology",
    "ovary": "Gynecology",
    "uterus": "Gynecology",
    # General Medicine
    "fever": "General Medicine",
    "cold": "General Medicine",
    "flu": "General Medicine",
    "cough": "General Medicine",
    "fatigue": "General Medicine",
    "weakness": "General Medicine",
    "diabetes": "General Medicine",
    "general checkup": "General Medicine",
    # Pediatrics
    "child": "Pediatrics",
    "baby": "Pediatrics",
    "infant": "Pediatrics",
    "vaccination": "Pediatrics",
    # Pulmonology
    "breathing": "Pulmonology",
    "asthma": "Pulmonology",
    "lung": "Pulmonology",
    "respiratory": "Pulmonology",
    "wheezing": "Pulmonology",
    # Ophthalmology
    "eye": "Ophthalmology",
    "vision": "Ophthalmology",
    "glasses": "Ophthalmology",
    "cataract": "Ophthalmology",
    # ENT
    "ear": "ENT",
    "nose": "ENT",
    "throat": "ENT",
    "sinus": "ENT",
    "tonsil": "ENT",
    "hearing": "ENT",
    # Psychiatry
    "anxiety": "Psychiatry",
    "depression": "Psychiatry",
    "stress": "Psychiatry",
    "insomnia": "Psychiatry",
    "mental health": "Psychiatry",
    "sleep": "Psychiatry",
    # Gastroenterology
    "stomach": "Gastroenterology",
    "digestion": "Gastroenterology",
    "liver": "Gastroenterology",
    "acid reflux": "Gastroenterology",
    "nausea": "Gastroenterology",
    "vomiting": "Gastroenterology",
    "abdominal pain": "Gastroenterology",
}


def search_doctors(speciality: str = None, hospital: str = None, doctor_name: str = None) -> list[dict]:
    """Search doctors with optional filters."""
    results = MOCK_DOCTORS.copy()

    if speciality:
        results = [d for d in results if speciality.lower() in d["speciality"].lower()]

    if hospital:
        results = [d for d in results if hospital.lower() in d["hospital"].lower()]

    if doctor_name:
        results = [d for d in results if doctor_name.lower() in d["name"].lower()]

    return results


def get_doctor_by_id(doctor_id: int) -> dict | None:
    """Get a specific doctor by ID."""
    for doc in MOCK_DOCTORS:
        if doc["doctor_id"] == doctor_id:
            return doc
    return None


def recommend_speciality(symptoms: str) -> str | None:
    """Match symptoms text to a speciality."""
    symptoms_lower = symptoms.lower()
    for keyword, spec in SYMPTOM_SPECIALITY_MAP.items():
        if keyword in symptoms_lower:
            return spec
    return None
