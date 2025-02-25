FROM python:3.9-slim

WORKDIR /app

# Install system dependencies with more comprehensive SSL certificate handling
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    openssl \
    curl \
    && update-ca-certificates \
    && curl -k https://curl.se/ca/cacert.pem -o /usr/local/share/ca-certificates/cacert.crt \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for SSL certificate handling
ENV SSL_CERT_DIR=/etc/ssl/certs
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV PYTHONHTTPSVERIFY=0

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
