# -------------------------------
# STAGE 1: Build environment
# -------------------------------

FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies (needed for psycopg2, etc.)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies to custom dir
COPY docker/requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# -------------------------------
# STAGE 2: Runtime environment
# -------------------------------

FROM python:3.9-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app files to the container
COPY app .

# Run the application
CMD ["python", "app.py"]