# Dockerfile
FROM python:3.10-slim

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the initialization script into the container
COPY data /data

# Command to run the script (adjust as necessary)
CMD ["sh", "-c", "sleep 30 && python /data_creator.py"]
