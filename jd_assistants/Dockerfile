FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy application code first
COPY src/ ./src/
COPY pyproject.toml ./

# Install Python dependencies (this will install the package)
RUN pip install --no-cache-dir -e .

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose ports
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "jd_assistants.api_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
