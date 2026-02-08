# Use official Python runtime as parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy poetry lock file and pyproject.toml
COPY backend/pyproject.toml backend/poetry.lock* ./

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main

# Copy the application code
COPY backend/src ./src
COPY backend/main.py ./main.py
COPY backend/init_db.py ./init_db.py
COPY backend/alembic.ini ./alembic.ini

# Expose the port the app runs on
EXPOSE 8000

# Start the FastAPI application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]