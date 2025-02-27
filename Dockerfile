# Start with a Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy application files from your local machine to the container
COPY . /app

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 4137

# Define the command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "timeCapsuleApi:app", "--port", "4137"]
