FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY soap_server.py .
COPY mock_client.py . 

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "soap_server:app", "--host", "0.0.0.0", "--port", "8000"]