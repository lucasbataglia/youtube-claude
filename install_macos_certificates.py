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
    print("Installing SSL certificates for Python on macOS...")
    
    # Get the current Python executable path
    python_exe = sys.executable
    print(f"Python executable: {python_exe}")
    
    # Get the certifi certificate path
    certifi_path = certifi.where()
    print(f"Certifi certificate path: {certifi_path}")
    
    # Create a directory for certificates
    ssl_dir = os.path.dirname(python_exe)
    os.makedirs(ssl_dir, exist_ok=True)
    print(f"SSL directory: {ssl_dir}")
    
    # Copy the certifi certificates to the SSL directory
    cert_file = os.path.join(ssl_dir, "cert.pem")
    with open(certifi_path, 'rb') as src, open(cert_file, 'wb') as dst:
        dst.write(src.read())
    print(f"Copied certificates to: {cert_file}")
    
    # Set environment variables
    os.environ['SSL_CERT_FILE'] = cert_file
    os.environ['REQUESTS_CA_BUNDLE'] = cert_file
    print("Set environment variables:")
    print(f"  SSL_CERT_FILE={cert_file}")
    print(f"  REQUESTS_CA_BUNDLE={cert_file}")
    
    # Run the macOS certificate installation command
    try:
        print("\nRunning macOS certificate installation command...")
        cmd = [
            "/Applications/Python 3.9/Install Certificates.command"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
        print(f"Command error: {result.stderr}")
    except Exception as e:
        print(f"Failed to run macOS certificate installation command: {str(e)}")
        print("Trying alternative approach...")
        
        # Alternative approach: Run the certificate installation directly
        try:
            import pip._vendor.certifi
            pip_certifi_path = pip._vendor.certifi.where()
            print(f"Pip certifi path: {pip_certifi_path}")
            
            # Create a temporary script
            script_content = f"""
            import os
            import ssl
            import certifi

            # Set environment variables
            os.environ['SSL_CERT_FILE'] = '{cert_file}'
            os.environ['REQUESTS_CA_BUNDLE'] = '{cert_file}'
            
            # Configure SSL context
            ssl._create_default_https_context = ssl.create_default_context
            """
            
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_ssl.py")
            with open(script_path, 'w') as f:
                f.write(script_content)
            print(f"Created temporary script: {script_path}")
            
            # Add to PYTHONSTARTUP
            print("To use this fix, add the following to your shell profile:")
            print(f"  export PYTHONSTARTUP={script_path}")
        except Exception as e:
            print(f"Alternative approach failed: {str(e)}")
    
    print("\nCertificate installation complete.")
    print("You may need to restart your Python applications for the changes to take effect.")
    print("You can also add these environment variables to your shell profile:")
    print(f"  export SSL_CERT_FILE={cert_file}")
    print(f"  export REQUESTS_CA_BUNDLE={cert_file}")

if __name__ == "__main__":
    main()
