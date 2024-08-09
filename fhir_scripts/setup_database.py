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
    password=db_password,
    host="127.0.0.1",
    port="5432"
)

# Set the isolation level to AUTOCOMMIT so we can create the database
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Create the FHIR API log database
cur.execute("CREATE DATABASE fhir_api_logs")

# Close the connection to the 'postgres' database
cur.close()
conn.close()

# Connect to the newly created 'fhir_api_logs' database
conn = psycopg2.connect(
    database="fhir_api_logs",
    user="postgres",
    password=db_password,
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

# Create the API logs table
create_logs_table = """
CREATE TABLE IF NOT EXISTS api_logs (
    log_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method VARCHAR(10),  -- GET, POST, PUT, DELETE
    endpoint VARCHAR(255),  -- e.g., /Patient
    resource_type VARCHAR(50),  -- Patient, Observation, etc.
    status_code INT,  -- HTTP status code
    request_payload JSONB,  -- Store the actual API request data
    response_payload JSONB  -- Store the response data
);
"""

cur.execute(create_logs_table)
conn.commit()

cur.close()
conn.close()

print("FHIR API log database and table created successfully.")
