# Dockerfile
FROM python:3.10-slim

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the initialization script into the container
COPY data_creator.py /data_creator.py
COPY data /data

# Command to run the script (adjust as necessary)
CMD ["sh", "-c", "sleep 10 && python /data_creator.py"]
