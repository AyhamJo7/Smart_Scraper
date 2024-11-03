# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright dependencies
RUN npm install -g playwright

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install Playwright browsers
RUN playwright install chromium

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "src/main.py"] 