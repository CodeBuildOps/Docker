# Use an official Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (psycopg2 needs libpq), curl for ping
RUN apt-get update \
    && apt-get install -y gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies, no cache to reduce image size
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files to the container
COPY app .

EXPOSE 5001

# Exposes a /health route in Flask app that returns 200 OK
# If not reachable, container is unhealthy
HEALTHCHECK --interval=10s --timeout=3s  --retries=3 CMD curl --fail http://localhost:5001/health || exit 1

# Run the application
CMD ["python", "app.py"]