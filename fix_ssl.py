import os
import ssl
import certifi

# Set environment variables
os.environ['SSL_CERT_FILE'] = '/Users/lucasfbataglia/Desktop/Python/youtube-claude/venv/bin/cert.pem'
os.environ['REQUESTS_CA_BUNDLE'] = '/Users/lucasfbataglia/Desktop/Python/youtube-claude/venv/bin/cert.pem'

# Configure SSL context
ssl._create_default_https_context = ssl.create_default_context
