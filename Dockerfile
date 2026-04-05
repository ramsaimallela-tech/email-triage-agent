FROM python:3.10

WORKDIR /code


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
