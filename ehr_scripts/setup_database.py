import psycopg2

# Connection details
conn = psycopg2.connect(
    database="ehr_db",
    user="postgres",
    password="gravityCache",
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
    phone_number VARCHAR(50),  -- Increased length to accommodate more formats
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

print("Database schema created successfully.")
