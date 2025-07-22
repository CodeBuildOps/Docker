# Use an official Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install (wget & unzip) for dockerize, then install Python dependencies (psycopg2 needs libpq)
RUN apt-get update \
    && apt-get install -y gcc libpq-dev wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Install dockerize (latest 0.6.1)
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz

# Copy requirements and install Python dependencies, no cache to reduce image size
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files to the container
COPY app .

# Run the application
CMD ["python", "app.py"]