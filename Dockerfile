FROM python:3.11-slim

# Metadata
LABEL maintainer="ramsaimallela-tech"
LABEL description="Email Triage Agent — OpenEnv AI Agent Environment"

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Create results directory
RUN mkdir -p results

# Default: run baseline evaluation across all 3 tasks
CMD ["python", "scripts/run_baseline.py"]
