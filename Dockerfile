# Use the official Python image as a base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY . .

# Expose port 8000 to allow external connections
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


## Use the official Python image as a base
#FROM python:3.10
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy the requirements file into the container
#COPY requirements.txt .
#
## Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy the Django project files into the container
#COPY . .
#
## Copy the .env file into the container
#COPY .env .
#
## Expose port 8000 to allow external connections
#EXPOSE 8000
#
## Load environment variables from .env file
#CMD ["sh", "-c", "source .env && python manage.py runserver 0.0.0.0:8000"]


