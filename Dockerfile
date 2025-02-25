FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create temp directory
RUN mkdir -p /app/temp && chmod 777 /app/temp

# Set environment variables
ENV PORT=5000
ENV WHISPER_MODEL=base
ENV TEMP_DIR=/app/temp
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the application with Gunicorn
CMD gunicorn --workers=2 --bind 0.0.0.0:$PORT app:app
