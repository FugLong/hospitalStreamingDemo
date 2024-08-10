#!/bin/sh

echo "run_generators.sh started....generation will begin in 20 seconds..."

# Add a delay to ensure the database setup is complete
sleep 20  # Wait for 10 seconds before starting data generators

# Run continuous data update
python /app/ehr_scripts/continuous_data_update.py &

# Run API faker
python /app/fhir_scripts/api_faker.py &

# Run event stream faker
python -u /app/kafka_scripts/fake_event_stream.py &

# Wait for all background jobs to finish
wait
