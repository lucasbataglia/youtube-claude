FROM python:3.9-slim

WORKDIR /app

# Install system dependencies with enhanced SSL certificate handling
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    openssl \
    curl \
    wget \
    python3-pip \
    && update-ca-certificates \
    && curl -k https://curl.se/ca/cacert.pem -o /usr/local/share/ca-certificates/cacert.crt \
    && curl -k https://www.amazontrust.com/repository/AmazonRootCA1.pem -o /usr/local/share/ca-certificates/AmazonRootCA1.crt \
    && curl -k https://letsencrypt.org/certs/isrgrootx1.pem -o /usr/local/share/ca-certificates/isrgrootx1.crt \
    && curl -k https://letsencrypt.org/certs/lets-encrypt-r3.pem -o /usr/local/share/ca-certificates/lets-encrypt-r3.crt \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install yt-dlp and pytube globally with specific versions
RUN pip install --no-cache-dir yt-dlp==2025.2.19 pytube>=12.1.0 certifi requests \
    && ln -sf /usr/local/bin/yt-dlp /usr/local/bin/youtube-dl

# Create directories for certificates
RUN mkdir -p /etc/ssl/certs/python /app/ssl

# Copy certifi certificates to a known location
RUN python -c "import certifi; import shutil; shutil.copy(certifi.where(), '/app/ssl/cert.pem')"

# Set environment variables for enhanced SSL certificate handling
ENV SSL_CERT_DIR=/etc/ssl/certs
ENV SSL_CERT_FILE=/app/ssl/cert.pem
ENV REQUESTS_CA_BUNDLE=/app/ssl/cert.pem
ENV PYTHONHTTPSVERIFY=0

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create SSL fix script
RUN echo 'import os\nimport ssl\nimport certifi\n\n# Set environment variables\nos.environ["SSL_CERT_FILE"] = "/app/ssl/cert.pem"\nos.environ["REQUESTS_CA_BUNDLE"] = "/app/ssl/cert.pem"\n\n# Configure SSL context\nssl._create_default_https_context = ssl.create_default_context' > /app/fix_ssl.py

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
