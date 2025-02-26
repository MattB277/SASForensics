# Use a Python image as the base
FROM python:3.9-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Set the working directory for the container
WORKDIR /app/backend

# Copy the backend code into the container
COPY ./sas-forensics/backend/ /app/backend/

# Set the working directory for the backend
# WORKDIR /backend

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory for the frontend
WORKDIR /app/frontend

# Copy the frontend code into the container
COPY sas-forensics/frontend/package.json /app/frontend/
COPY sas-forensics/frontend/package-lock.json /app/frontend/

# Install the npm dependencies for the frontend
RUN npm install

# Expose the ports for the frontend and backend
EXPOSE 8000
EXPOSE 3000

# Command to run both the frontend and backend using concurrently
CMD ["npm", "start"]
