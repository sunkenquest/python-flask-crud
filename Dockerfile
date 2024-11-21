# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/

# Create the virtual environment and install dependencies in a single layer
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . /app/

# Set the PATH to use the virtual environment's Python and pip
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port
EXPOSE 5000

# Define the command to run your app
CMD ["python", "main.py"]
