# Use an official Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (psycopg2 needs libpq)
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies, no cache to reduce image size
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and wait files to the container
COPY app .

# Run the application
CMD ["python", "app.py"]