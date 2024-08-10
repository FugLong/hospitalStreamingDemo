import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_password = os.getenv("POSTGRES_PASSWORD")

# Connect to the default 'postgres' database
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password=db_password,
    host="postgres",
    port="5432"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Terminate all connections to the existing ehr_db
try:
    cur.execute("""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = 'ehr_db' AND pid <> pg_backend_pid();
    """)
    print("Terminated all connections to ehr_db.")
except Exception as e:
    print(f"Error terminating connections: {e}")

# Drop the existing ehr_db if it exists
cur.execute("DROP DATABASE IF EXISTS ehr_db")
print("Dropped existing ehr_db database.")

# Create a fresh ehr_db
cur.execute("CREATE DATABASE ehr_db")
print("Created new ehr_db database.")

cur.close()
conn.close()

# Connect to the new ehr_db database
conn = psycopg2.connect(
    database="ehr_db",
    user="postgres",
    password=db_password,
    host="postgres",
    port="5432"
)
cur = conn.cursor()

# Define schema and ensure tables are created
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
