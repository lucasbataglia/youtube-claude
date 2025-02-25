#!/usr/bin/env python3
"""
Script to install SSL certificates for Python on macOS.
This is a common fix for SSL certificate verification issues on macOS.
"""

import os
import sys
import subprocess
import ssl
import certifi

def main():
    print("Installing SSL certificates for Python...")
    
    # Get the current Python executable path
    python_exe = sys.executable
    print(f"Python executable: {python_exe}")
    
    # Get the certifi certificate path
    certifi_path = certifi.where()
    print(f"Certifi certificate path: {certifi_path}")
    
    # Create a directory for certificates if it doesn't exist
    ssl_dir = os.path.join(os.path.dirname(python_exe), '..', 'etc', 'openssl')
    os.makedirs(ssl_dir, exist_ok=True)
    print(f"SSL directory: {ssl_dir}")
    
    # Copy the certifi certificates to the SSL directory
    cert_file = os.path.join(ssl_dir, 'cert.pem')
    with open(certifi_path, 'rb') as src, open(cert_file, 'wb') as dst:
        dst.write(src.read())
    print(f"Copied certificates to: {cert_file}")
    
    # Set environment variables
    os.environ['SSL_CERT_FILE'] = cert_file
    os.environ['REQUESTS_CA_BUNDLE'] = cert_file
    print("Set environment variables:")
    print(f"  SSL_CERT_FILE={cert_file}")
    print(f"  REQUESTS_CA_BUNDLE={cert_file}")
    
    # Test SSL connection
    try:
        print("\nTesting SSL connection to youtube.com...")
        context = ssl.create_default_context(cafile=cert_file)
        with ssl.create_connection(("youtube.com", 443)) as sock:
            with context.wrap_socket(sock, server_hostname="youtube.com") as ssock:
                print(f"SSL connection successful")
                print(f"SSL version: {ssock.version()}")
                print(f"Cipher: {ssock.cipher()}")
                print(f"Peer certificate: {ssock.getpeercert()}")
    except Exception as e:
        print(f"SSL connection test failed: {str(e)}")
    
    print("\nCertificate installation complete.")
    print("You may need to restart your Python applications for the changes to take effect.")
    print("You can also add these environment variables to your shell profile:")
    print(f"  export SSL_CERT_FILE={cert_file}")
    print(f"  export REQUESTS_CA_BUNDLE={cert_file}")

if __name__ == "__main__":
    main()
