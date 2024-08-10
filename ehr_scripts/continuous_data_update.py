import time
import random
import psycopg2
import uuid
import os
from dotenv import load_dotenv
from faker import Faker
import logging
import sys

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_password = os.getenv("POSTGRES_PASSWORD")

fake = Faker()

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='EHR - %(asctime)s - %(levelname)s - %(message)s'
)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="ehr_db",
    user="postgres",
    password=db_password,
    host="postgres",
    port="5432"
)
cur = conn.cursor()

def update_patient_info():
    cur.execute("SELECT patient_id FROM patients ORDER BY RANDOM() LIMIT 1")
    patient_id = cur.fetchone()[0]
    
    update_action = random.choice(['address', 'phone_number', 'email'])
    
    if update_action == 'address':
        new_address = fake.address()
        cur.execute("UPDATE patients SET address = %s WHERE patient_id = %s", (new_address, patient_id))
        logging.info(f"Updated address for patient {patient_id}")
    elif update_action == 'phone_number':
        new_phone_number = fake.phone_number()
        cur.execute("UPDATE patients SET phone_number = %s WHERE patient_id = %s", (new_phone_number, patient_id))
        logging.info(f"Updated phone number for patient {patient_id}")
    elif update_action == 'email':
        new_email = fake.email()
        cur.execute("UPDATE patients SET email = %s WHERE patient_id = %s", (new_email, patient_id))
        logging.info(f"Updated email for patient {patient_id}")

def add_new_encounter():
    cur.execute("SELECT patient_id FROM patients ORDER BY RANDOM() LIMIT 1")
    patient_id = cur.fetchone()[0]
    
    encounter_id = str(uuid.uuid4())
    date = fake.date_time_this_year()
    encounter_type = fake.random_element(elements=["Visit", "Surgery", "Consultation"])
    reason = fake.sentence(nb_words=6)
    physician = fake.name()
    notes = fake.paragraph(nb_sentences=3)
    
    cur.execute("""
        INSERT INTO encounters (encounter_id, patient_id, date, type, reason, physician, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (encounter_id, patient_id, date, encounter_type, reason, physician, notes))
    
    logging.info(f"Added new encounter {encounter_id} for patient {patient_id}")

def update_or_add_diagnosis():
    if random.choice([True, False]):
        cur.execute("SELECT diagnosis_id FROM diagnoses ORDER BY RANDOM() LIMIT 1")
        diagnosis_id = cur.fetchone()[0]
        new_description = fake.sentence(nb_words=5)
        cur.execute("UPDATE diagnoses SET description = %s WHERE diagnosis_id = %s", (new_description, diagnosis_id))
        logging.info(f"Updated diagnosis {diagnosis_id}")
    else:
        cur.execute("SELECT encounter_id, patient_id FROM encounters ORDER BY RANDOM() LIMIT 1")
        encounter_id, patient_id = cur.fetchone()
        diagnosis_id = str(uuid.uuid4())
        diagnosis_code = fake.lexify(text='???.??')
        description = fake.sentence(nb_words=5)
        cur.execute("""
            INSERT INTO diagnoses (diagnosis_id, encounter_id, patient_id, diagnosis_code, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (diagnosis_id, encounter_id, patient_id, diagnosis_code, description))
        logging.info(f"Added new diagnosis {diagnosis_id} for encounter {encounter_id}")

def add_new_lab_result():
    cur.execute("SELECT patient_id FROM patients ORDER BY RANDOM() LIMIT 1")
    patient_id = cur.fetchone()[0]
    
    lab_result_id = str(uuid.uuid4())
    test_name = fake.random_element(elements=["Blood Test", "X-ray", "MRI", "Ultrasound"])
    result_value = f"{fake.random_number(digits=3)}"
    normal_range = f"{fake.random_number(digits=2)}-{fake.random_number(digits=3)}"
    date_of_test = fake.date_this_year()
    status = fake.random_element(elements=["Normal", "Abnormal"])
    
    cur.execute("""
        INSERT INTO lab_results (lab_result_id, patient_id, test_name, result_value, normal_range, date_of_test, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (lab_result_id, patient_id, test_name, result_value, normal_range, date_of_test, status))
    
    logging.info(f"Added new lab result {lab_result_id} for patient {patient_id}")

try:
    while True:
        action = random.choice([update_patient_info, add_new_encounter, update_or_add_diagnosis, add_new_lab_result])
        action()
        conn.commit()
        time.sleep(random.randint(10, 30))
except KeyboardInterrupt:
    logging.info("Stopping continuous data updates.")
finally:
    cur.close()
    conn.close()
