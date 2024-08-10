from faker import Faker
import os
from dotenv import load_dotenv
import psycopg2
import uuid

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_password = os.getenv("POSTGRES_PASSWORD")

# Initialize Faker
fake = Faker()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="ehr_db",  # Change this if your database name is different
    user="postgres",
    password=db_password,
    host="postgres",
    port="5432"
)
cur = conn.cursor()

# Function to generate patient data
def generate_patient():
    patient_id = str(uuid.uuid4())
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    gender = fake.random_element(elements=("Male", "Female"))
    address = fake.address()
    phone_number = fake.phone_number()
    email = fake.email()
    primary_physician = fake.name()
    
    cur.execute("""
        INSERT INTO patients (patient_id, first_name, last_name, dob, gender, address, phone_number, email, primary_physician)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (patient_id, first_name, last_name, dob, gender, address, phone_number, email, primary_physician))
    
    return patient_id

# Function to generate encounters data
def generate_encounter(patient_id):
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
    
    return encounter_id

# Function to generate diagnosis data
def generate_diagnosis(encounter_id, patient_id):
    diagnosis_id = str(uuid.uuid4())
    diagnosis_code = fake.lexify(text='???.??')  # Random ICD-10 code pattern
    description = fake.sentence(nb_words=5)
    
    cur.execute("""
        INSERT INTO diagnoses (diagnosis_id, encounter_id, patient_id, diagnosis_code, description)
        VALUES (%s, %s, %s, %s, %s)
    """, (diagnosis_id, encounter_id, patient_id, diagnosis_code, description))

# Function to generate medication data
def generate_medication(patient_id):
    medication_id = str(uuid.uuid4())
    name = fake.lexify(text='Medication ???')
    dosage = fake.numerify(text='## mg')
    start_date = fake.date_this_year()
    end_date = fake.date_between(start_date=start_date, end_date="+30d")
    prescribing_physician = fake.name()
    
    cur.execute("""
        INSERT INTO medications (medication_id, patient_id, name, dosage, start_date, end_date, prescribing_physician)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (medication_id, patient_id, name, dosage, start_date, end_date, prescribing_physician))

# Function to generate lab results data
def generate_lab_result(patient_id):
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

# Populate database with data
def populate_database(num_patients):
    for _ in range(num_patients):
        patient_id = generate_patient()
        for _ in range(fake.random_int(min=1, max=3)):
            encounter_id = generate_encounter(patient_id)
            generate_diagnosis(encounter_id, patient_id)
        for _ in range(fake.random_int(min=1, max=3)):
            generate_medication(patient_id)
        for _ in range(fake.random_int(min=1, max=3)):
            generate_lab_result(patient_id)
        conn.commit()

# Example usage: Populate the database with 10 patients and associated data
populate_database(10)

# Close the cursor and connection
cur.close()
conn.close()

print("Database populated with realistic data.")
