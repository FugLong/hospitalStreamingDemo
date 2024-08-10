#!/bin/sh

# Wait until PostgreSQL is available
until nc -z -v -w30 postgres 5432
do
  echo "Waiting for PostgreSQL database connection..."
  sleep 1
done
echo "PostgreSQL is up - executing commands"

# Run the setup scripts
python /app/ehr_scripts/setup_database.py
python /app/fhir_scripts/setup_database.py

# Populate the databases
python /app/ehr_scripts/populate_database.py
python /app/fhir_scripts/populate_database.py

echo "Database setup and population complete."

# Check if the data generator should be started
if [ "$GENERATOR_ENABLED" = "true" ]; then
    echo "Starting data generators..."
    /app/data_generator/run_generators.sh &
else
    echo "Data generators are disabled."
fi

# Keep the container running
tail -f /dev/null
