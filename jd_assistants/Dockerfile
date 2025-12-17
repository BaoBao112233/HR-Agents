FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy application code first
COPY src/ ./src/
COPY pyproject.toml ./

# Install Python dependencies (this will install the package)
RUN pip install --no-cache-dir -e .

# Copy frontend code
COPY frontend/ ./frontend/

# Build frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Move built files to static directory
WORKDIR /app
RUN mkdir -p /app/static && \
    cp -r /app/frontend/dist/* /app/static/ && \
    rm -rf /app/frontend/node_modules

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "jd_assistants.api_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
