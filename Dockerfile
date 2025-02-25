FROM python:3.9-slim

WORKDIR /app

# Install system dependencies with more comprehensive SSL certificate handling
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    openssl \
    curl \
    wget \
    python3-pip \
    && update-ca-certificates \
    && curl -k https://curl.se/ca/cacert.pem -o /usr/local/share/ca-certificates/cacert.crt \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install yt-dlp globally to ensure it's available as a command
RUN pip install --no-cache-dir yt-dlp==2025.2.19 pytube>=12.1.0 \
    && ln -sf /usr/local/bin/yt-dlp /usr/local/bin/youtube-dl

# Create a directory for certificates
RUN mkdir -p /etc/ssl/certs/python

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
