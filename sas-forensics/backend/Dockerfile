# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire backend directory
COPY backend/ .

# Create a virtual environment
RUN python -m venv /myenv
ENV PATH="/myenv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Create static files directory
RUN mkdir -p /app/staticfiles

# Collect static files (this assumes you've added STATIC_ROOT to settings.py)
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]