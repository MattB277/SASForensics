# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0  # Production default, override locally if needed

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

# Create directories for static files and media
RUN mkdir -p /app/staticfiles /app/media

# Collect static files (uses STATIC_ROOT from settings.py)
RUN python manage.py collectstatic --noinput

# Expose the port (EB uses 8000 by default)
EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend_core.wsgi:application"]