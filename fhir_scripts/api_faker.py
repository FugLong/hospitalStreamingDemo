import logging
import os
import sys
import psycopg2
import random
import time
import uuid
import json
from dotenv import load_dotenv
from faker import Faker

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_password = os.getenv("POSTGRES_PASSWORD")

# Initialize Faker
fake = Faker()

# Configure logging for FHIR
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='FHIR - %(asctime)s - %(levelname)s - %(message)s'
)

# Connect to the PostgreSQL databases
ehr_conn = psycopg2.connect(
    database="ehr_db",
    user="postgres",
    password=db_password,
    host="postgres",
    port="5432"
)
ehr_cur = ehr_conn.cursor()

fhir_conn = psycopg2.connect(
    database="fhir_api_logs",
    user="postgres",
    password=db_password,
    host="postgres",
    port="5432"
)
fhir_cur = fhir_conn.cursor()

# Function to log API requests
def log_api_request(method, endpoint, resource_type, status_code, request_payload, response_payload):
    fhir_cur.execute("""
        INSERT INTO api_logs (method, endpoint, resource_type, status_code, request_payload, response_payload)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (method, endpoint, resource_type, status_code, json.dumps(request_payload), json.dumps(response_payload)))
    fhir_conn.commit()
    logging.info(f"Logged API request to {endpoint} for resource {resource_type} with status {status_code}")

# Function to simulate creating a patient
def create_patient():
    patient_id = str(uuid.uuid4())
    patient_data = {
        "id": patient_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "gender": fake.random_element(elements=("Male", "Female")),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "primary_physician": fake.name()
    }
    
    # Insert into EHR database
    ehr_cur.execute("""
        INSERT INTO patients (patient_id, first_name, last_name, dob, gender, address, phone_number, email, primary_physician)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (patient_data["id"], patient_data["first_name"], patient_data["last_name"], patient_data["dob"], patient_data["gender"], patient_data["address"], patient_data["phone_number"], patient_data["email"], patient_data["primary_physician"]))
    ehr_conn.commit()
    
    # Log the API request
    log_api_request(
        method="POST",
        endpoint="/Patient",
        resource_type="Patient",
        status_code=201,
        request_payload=patient_data,
        response_payload={"id": patient_id, "status": "created"}
    )

    logging.info(f"Created patient {patient_id}")

# Function to simulate adding an observation
def add_observation():
    ehr_cur.execute("SELECT patient_id FROM patients ORDER BY RANDOM() LIMIT 1")
    patient_id = ehr_cur.fetchone()[0]
    
    observation_id = str(uuid.uuid4())
    observation_data = {
        "id": observation_id,
        "patient_id": patient_id,
        "type": fake.random_element(elements=["Blood Pressure", "Heart Rate", "Glucose"]),
        "value": fake.random_int(min=70, max=180),
        "date": fake.date_time_this_year().isoformat()
    }
    
    # Insert into EHR database
    ehr_cur.execute("""
        INSERT INTO lab_results (lab_result_id, patient_id, test_name, result_value, date_of_test, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (observation_data["id"], observation_data["patient_id"], observation_data["type"], str(observation_data["value"]), observation_data["date"], "Normal"))
    ehr_conn.commit()
    
    # Log the API request
    log_api_request(
        method="POST",
        endpoint="/Observation",
        resource_type="Observation",
        status_code=201,
        request_payload=observation_data,
        response_payload={"id": observation_id, "status": "created"}
    )

    logging.info(f"Added observation {observation_id} for patient {patient_id}")

# Function to simulate creating an encounter
def create_encounter():
    ehr_cur.execute("SELECT patient_id FROM patients ORDER BY RANDOM() LIMIT 1")
    patient_id = ehr_cur.fetchone()[0]
    
    encounter_id = str(uuid.uuid4())
    encounter_data = {
        "id": encounter_id,
        "patient_id": patient_id,
        "date": fake.date_time_this_year().isoformat(),
        "type": fake.random_element(elements=["Consultation", "Surgery", "Emergency"]),
        "reason": fake.sentence(nb_words=6),
        "physician": fake.name(),
        "notes": fake.paragraph(nb_sentences=3)
    }
    
    # Insert into EHR database
    ehr_cur.execute("""
        INSERT INTO encounters (encounter_id, patient_id, date, type, reason, physician, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (encounter_data["id"], encounter_data["patient_id"], encounter_data["date"], encounter_data["type"], encounter_data["reason"], encounter_data["physician"], encounter_data["notes"]))
    ehr_conn.commit()
    
    # Log the API request
    log_api_request(
        method="POST",
        endpoint="/Encounter",
        resource_type="Encounter",
        status_code=201,
        request_payload=encounter_data,
        response_payload={"id": encounter_id, "status": "created"}
    )

    logging.info(f"Created encounter {encounter_id} for patient {patient_id}")

# Function to simulate adding a medication
def add_medication():
    ehr_cur.execute("SELECT patient_id FROM patients ORDER BY RANDOM() LIMIT 1")
    patient_id = ehr_cur.fetchone()[0]
    
    medication_id = str(uuid.uuid4())
    medication_data = {
        "id": medication_id,
        "patient_id": patient_id,
        "name": fake.lexify(text="Medication ???"),
        "dosage": fake.numerify(text="## mg"),
        "start_date": fake.date_this_year().isoformat(),
        "end_date": fake.date_between(start_date="today", end_date="+30d").isoformat(),
        "prescribing_physician": fake.name()
    }
    
    # Insert into EHR database
    ehr_cur.execute("""
        INSERT INTO medications (medication_id, patient_id, name, dosage, start_date, end_date, prescribing_physician)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (medication_data["id"], medication_data["patient_id"], medication_data["name"], medication_data["dosage"], medication_data["start_date"], medication_data["end_date"], medication_data["prescribing_physician"]))
    ehr_conn.commit()
    
    # Log the API request
    log_api_request(
        method="POST",
        endpoint="/Medication",
        resource_type="Medication",
        status_code=201,
        request_payload=medication_data,
        response_payload={"id": medication_id, "status": "created"}
    )

    logging.info(f"Added medication {medication_id} for patient {patient_id}")

# Function to simulate the API faker running continuously
def run_api_faker():
    actions = [create_patient, add_observation, create_encounter, add_medication]
    try:
        while True:
            action = random.choice(actions)
            action()
            time.sleep(random.randint(5, 15))  # Wait between actions
    except KeyboardInterrupt:
        logging.info("API faker stopped.")
    finally:
        ehr_cur.close()
        ehr_conn.close()
        fhir_cur.close()
        fhir_conn.close()

if __name__ == "__main__":
    run_api_faker()
