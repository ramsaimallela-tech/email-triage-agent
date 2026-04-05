FROM python:3.11

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for Gradio
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Start the unified API + UI server
CMD ["python", "api.py"]
