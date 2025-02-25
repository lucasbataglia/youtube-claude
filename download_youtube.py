#!/usr/bin/env python3
"""
Simple script to download a YouTube video using yt-dlp with various workarounds.
"""

import os
import sys
import ssl
import certifi
import subprocess
import tempfile
import shutil

# Configure SSL with certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl._create_default_https_context = lambda: ssl_context

# Set environment variables for SSL
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['PYTHONHTTPSVERIFY'] = '0'

def download_with_yt_dlp_command(url, output_path):
    """Download YouTube video using yt-dlp command line with all possible workarounds."""
    print(f"Downloading {url} to {output_path}")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="yt-dlp-")
    temp_output = os.path.join(temp_dir, "audio.%(ext)s")
    
    try:
        # Construct command with all possible workarounds
        cmd = [
            "yt-dlp",
            "--no-check-certificate",  # Ignore SSL certificate verification
            "--no-cache-dir",          # Disable cache
            "--geo-bypass",            # Bypass geo-restrictions
            "--force-ipv4",            # Force IPv4
            "--ignore-errors",         # Continue on download errors
            "--no-warnings",           # Suppress warnings
            "--prefer-insecure",       # Prefer insecure connections
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--extract-audio",         # Extract audio
            "--audio-format", "mp3",   # Convert to mp3
            "--audio-quality", "192k", # Set audio quality
            "--output", temp_output,   # Set output template
            url                        # YouTube URL
        ]
        
        # Run command
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check if command was successful
        if result.returncode != 0:
            print(f"Command failed with code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        
        # Find the output file
        for file in os.listdir(temp_dir):
            if file.endswith(".mp3"):
                mp3_path = os.path.join(temp_dir, file)
                # Copy to final destination
                shutil.copy2(mp3_path, output_path)
                print(f"Downloaded to {output_path}")
                return True
        
        print("No MP3 file found in output directory")
        return False
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def download_with_pytube(url, output_path):
    """Download YouTube video using pytube."""
    print(f"Downloading {url} to {output_path} using pytube")
    
    try:
        from pytube import YouTube
        
        # Create YouTube object
        yt = YouTube(url)
        
        # Get audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            print("No audio stream found")
            return False
        
        # Download audio
        temp_dir = tempfile.mkdtemp(prefix="pytube-")
        audio_file = audio_stream.download(output_path=temp_dir)
        
        # Convert to mp3 using ffmpeg
        try:
            # Construct ffmpeg command
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", audio_file,
                "-vn",  # No video
                "-ar", "44100",  # Audio sampling rate
                "-ac", "2",  # Stereo
                "-b:a", "192k",  # Bitrate
                "-f", "mp3",  # Format
                output_path
            ]
            
            # Run ffmpeg
            subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print(f"Converted to MP3: {output_path}")
            
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"Failed to convert to MP3: {e}")
            # If conversion failed, just copy the file
            shutil.copy2(audio_file, output_path)
        
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return os.path.exists(output_path)
        
    except Exception as e:
        print(f"Pytube error: {e}")
        return False

def download_with_youtube_dl(url, output_path):
    """Download YouTube video using youtube-dl command."""
    print(f"Downloading {url} to {output_path} using youtube-dl")
    
    try:
        # Construct command
        cmd = [
            "youtube-dl",
            "--no-check-certificate",
            "--no-cache-dir",
            "--geo-bypass",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "192k",
            "-o", output_path,
            url
        ]
        
        # Run command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check if command was successful
        if result.returncode != 0:
            print(f"Command failed with code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        
        return os.path.exists(output_path)
        
    except Exception as e:
        print(f"youtube-dl error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_youtube.py <youtube_url> [output_path]")
        return 1
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"
    
    print(f"Downloading {url} to {output_path}")
    
    # Try all methods
    methods = [
        download_with_yt_dlp_command,
        download_with_pytube,
        download_with_youtube_dl
    ]
    
    for method in methods:
        print(f"\nTrying method: {method.__name__}")
        if method(url, output_path):
            print(f"\nDownload successful using {method.__name__}")
            return 0
    
    print("\nAll download methods failed")
    return 1

if __name__ == "__main__":
    sys.exit(main())
