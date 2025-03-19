FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY mock_client.py .
COPY soap_server.py .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "soap_server.py"]