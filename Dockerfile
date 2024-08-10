FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Wait for PostgreSQL to be ready before running scripts
RUN apt-get update && apt-get install -y netcat-openbsd

# Run the setup and population scripts
CMD ["sh", "/app/run_setup.sh"]
