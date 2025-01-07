# Use the official Python image as the base
#FROM python:3.13-slim
FROM python:3.13-alpine

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the scheduler script
CMD ["python", "-u", "main.py"]
