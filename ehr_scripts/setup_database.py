import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_password = os.getenv("POSTGRES_PASSWORD")

# Connect to the default 'postgres' database
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password=db_password,  # Replace with your actual password
    host="127.0.0.1",
    port="5432"
)

# Set the isolation level to AUTOCOMMIT so we can create the database
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Create the EHR database
cur.execute("CREATE DATABASE ehr_db")

# Close the connection to the 'postgres' database
cur.close()
conn.close()

# Connect to the newly created 'ehr_db' database
conn = psycopg2.connect(
    database="ehr_db",
    user="postgres",
    password=db_password,  # Replace with your actual password
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

# Define schema
create_tables = """
CREATE TABLE IF NOT EXISTS patients (
    patient_id UUID PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob DATE,
    gender VARCHAR(10),
    address TEXT,
    phone_number VARCHAR(50),
    email VARCHAR(100),
    primary_physician VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS encounters (
    encounter_id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(patient_id),
    date TIMESTAMP,
    type VARCHAR(50),
    reason TEXT,
    physician VARCHAR(100),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id UUID PRIMARY KEY,
    encounter_id UUID REFERENCES encounters(encounter_id),
    patient_id UUID REFERENCES patients(patient_id),
    diagnosis_code VARCHAR(10),
    description TEXT
);

CREATE TABLE IF NOT EXISTS medications (
    medication_id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(patient_id),
    name VARCHAR(100),
    dosage VARCHAR(50),
    start_date DATE,
    end_date DATE,
    prescribing_physician VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS lab_results (
    lab_result_id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(patient_id),
    test_name VARCHAR(100),
    result_value VARCHAR(50),
    normal_range VARCHAR(50),
    date_of_test DATE,
    status VARCHAR(20)
);
"""

cur.execute(create_tables)
conn.commit()

cur.close()
conn.close()

print("EHR database and tables created successfully.")
