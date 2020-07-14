# Build base image
FROM python:3.8.2

# Create app directory
RUN mkdir /code
WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install netcat
RUN apt-get update && apt-get install -y netcat

# Upgrade PIP
RUN pip install --upgrade pip

# Copy requirements and install them
COPY requirements.txt setup.py tox.ini entrypoint.sh ./
RUN pip install -r requirements.txt
RUN pip install -e .

# Copy directories
COPY qpcr_manager qpcr_manager/
COPY temp temp/

# Expose port
EXPOSE 5000
