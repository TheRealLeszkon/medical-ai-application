#!/bin/bash

# Ensure your FastAPI server is running before executing this script!
API_URL="http://127.0.0.1:8000"

# Define realistic patient names
PATIENT_NAMES=("John Doe" "Jane Smith" "Michael Johnson" "Emily Davis" "William Brown" "Olivia Wilson")
PATIENT_LEGAL_NAMES=("Johnathan Richard Doe" "Jane Marie Smith" "Michael David Johnson" "Emily Rose Davis" "William Thomas Brown" "Olivia Grace Wilson")

# Arrays to hold the dynamic IDs returned from the API
CREATED_PATIENT_IDS=()
CREATED_DOCTOR_IDS=()

echo "--- Seeding 6 Patients ---"
for i in {0..5}; do
  id=$((i+1))
  RESPONSE=$(curl -s -X POST "$API_URL/patients/" \
       -H "Content-Type: application/json" \
       -d '{
         "name": "'"${PATIENT_NAMES[$i]}"'",
         "full_legal_name": "'"${PATIENT_LEGAL_NAMES[$i]}"'",
         "date_of_birth": "199'"$id"'-01-01",
         "blood_group": "O+",
         "government_id_number": "GOV-P-'"$RANDOM"'",
         "phone_number": "555-010'"$id"'",
         "emergency_contact": "555-020'"$id"'"
       }')
  
  echo "$RESPONSE"
  
  # Extract patient_id using grep and cut to avoid python dependency issues
  PID=$(echo "$RESPONSE" | grep -o '"patient_id":[0-9]*' | cut -d: -f2)
  CREATED_PATIENT_IDS+=("$PID")
done

# Define realistic doctor names and specialties
DOCTOR_NAMES=("Dr. Gregory House" "Dr. Meredith Grey" "Dr. Derek Shepherd" "Dr. Cristina Yang" "Dr. Stephen Strange" "Dr. John Watson")
DOCTOR_SPECS=("Neurology" "Cardiology" "Neurology" "Cardiology" "Neurology" "Cardiology")

echo -e "\n--- Seeding 6 Doctors ---"
for i in {0..5}; do
  id=$((i+1))
  RESPONSE=$(curl -s -X POST "$API_URL/doctors/" \
       -H "Content-Type: application/json" \
       -d '{
         "medical_license_number": "LIC-D-'"$RANDOM"'",
         "speciality": "'"${DOCTOR_SPECS[$i]}"'",
         "qualifications": "MD",
         "experience_years": '"$id"',
         "workplace_hospital": "City General Hospital",
         "languages": "English",
         "availability_hours": "9AM - 5PM",
         "consultation_fees": '"$((100 + id * 10))"'
       }')
       
  echo "$RESPONSE"
  
  DID=$(echo "$RESPONSE" | grep -o '"doctor_id":[0-9]*' | cut -d: -f2)
  CREATED_DOCTOR_IDS+=("$DID")
done

echo -e "\n--- Seeding 6 Medical Documents ---"
for i in {0..5}; do
  PID="${CREATED_PATIENT_IDS[$i]}"
  if [ -z "$PID" ]; then continue; fi
  
  # Create a temporary dummy text file
  echo "This is the content for medical document belonging to patient ID $PID." > "dummy_$PID.txt"
  
  curl -s -X POST "$API_URL/medical-records/" \
       -F "patient_id=$PID" \
       -F "file=@dummy_$PID.txt"
  echo ""
  
  # Clean up dummy file
  rm "dummy_$PID.txt"
done

echo -e "\n--- Seeding 6 Appointments ---"
for i in {0..5}; do
  PID="${CREATED_PATIENT_IDS[$i]}"
  DID="${CREATED_DOCTOR_IDS[$i]}"
  if [ -z "$PID" ] || [ -z "$DID" ]; then continue; fi

  curl -s -X POST "$API_URL/appointments/" \
       -H "Content-Type: application/json" \
       -d '{
         "patient_id": '"$PID"',
         "doctor_id": '"$DID"',
         "booked_datetime": "2026-06-0'"$((i+1))"'T10:00:00",
         "reason": "Routine Checkup '"$((i+1))"'"
       }'
  echo ""
done

echo -e "\nDone!"
