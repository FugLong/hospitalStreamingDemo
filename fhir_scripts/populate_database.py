from faker import Faker
import os
from dotenv import load_dotenv
import psycopg2
import json
import uuid

# Load environment variables from .env file
load_dotenv()

# Get the database password from the environment variable
db_password = os.getenv("POSTGRES_PASSWORD")

# Initialize Faker
fake = Faker()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="fhir_api_logs",
    user="postgres",
    password=db_password,
    host="postgres",
    port="5432"
)
cur = conn.cursor()

# Function to populate the API logs
def populate_api_logs(num_entries):
    for _ in range(num_entries):
        method = fake.random_element(elements=("GET", "POST", "PUT", "DELETE"))
        endpoint = fake.random_element(elements=("/Patient", "/Observation", "/Encounter"))
        resource_type = endpoint.strip("/")
        status_code = fake.random_element(elements=(200, 201, 400, 404, 500))
        
        # Simulate a request and response payload
        request_payload = {
            "id": str(uuid.uuid4()),
            "name": fake.name(),
            "birthdate": fake.date_of_birth().isoformat(),
            "resourceType": resource_type
        }
        
        response_payload = {
            "status": "success" if status_code in (200, 201) else "error",
            "id": request_payload["id"],
            "resourceType": resource_type
        }

        # Insert log into the database
        cur.execute("""
            INSERT INTO api_logs (method, endpoint, resource_type, status_code, request_payload, response_payload)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (method, endpoint, resource_type, status_code, json.dumps(request_payload), json.dumps(response_payload)))

    conn.commit()

# Example usage: Populate the database with 100 log entries
populate_api_logs(100)

cur.close()
conn.close()

print("FHIR API logs populated successfully.")
