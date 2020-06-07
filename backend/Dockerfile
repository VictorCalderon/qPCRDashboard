# Build base image
FROM python:3.8

# Create app directory
RUN mkdir /code
WORKDIR /code

# Copy requirements and install them
COPY requirements.txt setup.py tox.ini ./
RUN pip install -r requirements.txt
RUN pip install -e .

# Copy directories
COPY corona corona/
COPY projects projects/

# Expose port
EXPOSE 5000
