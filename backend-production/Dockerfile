# Use python 3.9.18-bullseye
FROM python:3.9.18-bullseye

# Expose port
EXPOSE 8000

# Enable Python buffered write
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Change working directory
WORKDIR /app

# Copy requirements-production.txt file to install
COPY ./requirements-production.txt .

# Install requirements
RUN pip install -r requirements-production.txt

# Copy necessary files
COPY . .

# Run run.sh script when container starts
ENTRYPOINT ["/bin/bash", "./run.sh"]
