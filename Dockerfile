# Multi-stage production container for PragyanAI-SpecForge
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /workspace

# Install system dependencies & EDA simulation toolchains
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    iverilog \
    libmagic1 \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source tree
COPY . .

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Healthcheck targeting FastAPI
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default execution starts FastAPI backend server
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
