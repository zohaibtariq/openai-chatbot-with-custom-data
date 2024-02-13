# Use Python slim image version 3.11.7
FROM python:3.11.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Create a new virtual environment
RUN python -m venv venv

# Make the activate script executable
RUN chmod +x venv/bin/activate

# Activate the virtual environment
#RUN /bin/bash -c "venv/bin/activate" # working
RUN "venv/bin/activate"  # working

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Activate the virtual environment and upgrade pip
#RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir --upgrade pip" # working

# Install dependencies from requirements.txt
#RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt" # working

# Copy the content of the local app directory to the working directory
COPY app/ .

# Default values for host and port (can be overridden during build)
ARG FLASK_RUN_HOST=0.0.0.0
ARG FLASK_RUN_PORT=1000

# Set environment variables
ENV FLASK_RUN_HOST=$FLASK_RUN_HOST
ENV FLASK_RUN_PORT=$FLASK_RUN_PORT

EXPOSE ${FLASK_RUN_PORT}

CMD flask run --host=$FLASK_RUN_HOST --port=$FLASK_RUN_PORT --reload

