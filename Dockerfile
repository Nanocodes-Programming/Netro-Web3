# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for Python and Django
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the Django project source code into the container
COPY . /app/

# Start Gunicorn to serve your Django application
CMD ["gunicorn", "app", "app", ]
