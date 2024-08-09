import time
import random
import psycopg2
import uuid
import os
from dotenv import load_dotenv
from faker import Faker

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_password = os.getenv("POSTGRES_PASSWORD")

fake = Faker()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="ehr_db",
    user="postgres",
    password=db_password,
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

def update_patient_info():
    # Select a random patient to update
    cur.execute("SELECT patient_id FROM patients ORDER BY RANDOM() LIMIT 1")
    patient_id = cur.fetchone()[0]
    
    # Randomly choose an update action
    update_action = random.choice(['address', 'phone_number', 'email'])
    
    if update_action == 'address':
        new_address = fake.address()
        cur.execute("UPDATE patients SET address = %s WHERE patient_id = %s", (new_address, patient_id))
    elif update_action == 'phone_number':
        new_phone_number = fake.phone_number()
        cur.execute("UPDATE patients SET phone_number = %s WHERE patient_id = %s", (new_phone_number, patient_id))
    elif update_action == 'email':
        new_email = fake.email()
        cur.execute("UPDATE patients SET email = %s WHERE patient_id = %s", (new_email, patient_id))
    
    print(f"Updated {update_action} for patient {patient_id}")

def add_new_encounter():
    # Select a random patient to add an encounter
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
    
    print(f"Added new encounter {encounter_id} for patient {patient_id}")

def update_or_add_diagnosis():
    # 50% chance to update an existing diagnosis or add a new one
    if random.choice([True, False]):
        cur.execute("SELECT diagnosis_id FROM diagnoses ORDER BY RANDOM() LIMIT 1")
        diagnosis_id = cur.fetchone()[0]
        new_description = fake.sentence(nb_words=5)
        cur.execute("UPDATE diagnoses SET description = %s WHERE diagnosis_id = %s", (new_description, diagnosis_id))
        print(f"Updated diagnosis {diagnosis_id}")
    else:
        # Add a new diagnosis
        cur.execute("SELECT encounter_id, patient_id FROM encounters ORDER BY RANDOM() LIMIT 1")
        encounter_id, patient_id = cur.fetchone()
        diagnosis_id = str(uuid.uuid4())
        diagnosis_code = fake.lexify(text='???.??')  # Random ICD-10 code pattern
        description = fake.sentence(nb_words=5)
        cur.execute("""
            INSERT INTO diagnoses (diagnosis_id, encounter_id, patient_id, diagnosis_code, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (diagnosis_id, encounter_id, patient_id, diagnosis_code, description))
        print(f"Added new diagnosis {diagnosis_id} for encounter {encounter_id}")

def add_new_lab_result():
    # Select a random patient to add a lab result
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
    
    print(f"Added new lab result {lab_result_id} for patient {patient_id}")

# Continuous data generation
try:
    while True:
        action = random.choice([update_patient_info, add_new_encounter, update_or_add_diagnosis, add_new_lab_result])
        action()
        conn.commit()
        time.sleep(random.randint(10, 30))  # Pause for a random time between actions
except KeyboardInterrupt:
    print("Stopping continuous data updates.")

finally:
    cur.close()
    conn.close()
