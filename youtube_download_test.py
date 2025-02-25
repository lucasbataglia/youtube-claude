#!/usr/bin/env python3
"""
YouTube Download Test Script

This script tests different methods and configurations for downloading YouTube videos
to help diagnose and troubleshoot issues with YouTube downloads.
"""

import os
import sys
import argparse
import logging
import tempfile
import subprocess
import ssl
import certifi
import urllib.request
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("youtube-test")

def configure_ssl():
    """Configure SSL with multiple fallback options."""
    logger.info("Configuring SSL...")
    
    # Method 1: Use certifi
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl._create_default_https_context = lambda: ssl_context
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        logger.info("SSL configured with certifi")
    except Exception as e:
        logger.warning(f"Failed to configure SSL with certifi: {str(e)}")
        
        # Method 2: Disable SSL verification completely
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            logger.info("SSL verification disabled")
        except Exception as e:
            logger.error(f"Failed to disable SSL verification: {str(e)}")
    
    # Set environment variable for subprocesses
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    logger.info("Set PYTHONHTTPSVERIFY=0 for subprocesses")

def test_url_access(url):
    """Test if a URL is accessible."""
    logger.info(f"Testing URL access: {url}")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            status = response.status
            logger.info(f"URL access successful: Status {status}")
            return True
    except Exception as e:
        logger.error(f"URL access failed: {str(e)}")
        return False

def get_video_info(video_id):
    """Try to get video info using YouTube API."""
    logger.info(f"Getting video info for ID: {video_id}")
    
    # Try different API endpoints
    endpoints = [
        f"https://www.youtube.com/watch?v={video_id}",
        f"https://www.youtube.com/get_video_info?video_id={video_id}",
        f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    ]
    
    for endpoint in endpoints:
        try:
            logger.info(f"Trying endpoint: {endpoint}")
            with urllib.request.urlopen(endpoint, timeout=10) as response:
                if response.status == 200:
                    if endpoint.endswith('json'):
                        data = json.loads(response.read().decode('utf-8'))
                        logger.info(f"Video info: {data}")
                    else:
                        logger.info(f"Endpoint {endpoint} accessible")
                    return True
        except Exception as e:
            logger.warning(f"Failed to access {endpoint}: {str(e)}")
    
    logger.error("All video info endpoints failed")
    return False

def test_yt_dlp_python(url, temp_dir):
    """Test downloading with yt-dlp Python library."""
    logger.info("Testing yt-dlp Python library...")
    
    try:
        import yt_dlp
        
        # Different option sets to try
        option_sets = [
            # Basic options
            {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, "test1.%(ext)s"),
                'nocheckcertificate': True,
                'geo_bypass': True,
            },
            
            # Advanced options
            {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, "test2.%(ext)s"),
                'nocheckcertificate': True,
                'geo_bypass': True,
                'force_generic_extractor': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            },
            
            # Minimal options
            {
                'format': 'worst',  # Try lowest quality
                'outtmpl': os.path.join(temp_dir, "test3.%(ext)s"),
                'nocheckcertificate': True,
                'geo_bypass': True,
                'skip_download': True,  # Just get info, don't download
            }
        ]
        
        for i, options in enumerate(option_sets):
            logger.info(f"Trying option set {i+1}...")
            try:
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=not options.get('skip_download', False))
                    if info:
                        logger.info(f"Option set {i+1} successful")
                        if 'title' in info:
                            logger.info(f"Video title: {info['title']}")
                        return True
            except Exception as e:
                logger.warning(f"Option set {i+1} failed: {str(e)}")
        
        logger.error("All yt-dlp Python options failed")
        return False
        
    except ImportError:
        logger.error("yt-dlp Python library not installed")
        return False

def test_yt_dlp_command(url, temp_dir):
    """Test downloading with yt-dlp command line."""
    logger.info("Testing yt-dlp command line...")
    
    # Different command sets to try
    command_sets = [
        # Basic command
        ["yt-dlp", "--no-check-certificate", "--geo-bypass", "-f", "bestaudio/best", "-o", 
         os.path.join(temp_dir, "cmd1.%(ext)s"), url],
        
        # Advanced command
        ["yt-dlp", "--no-check-certificate", "--geo-bypass", "--force-ipv4", "--force-generic-extractor",
         "--extractor-args", "youtube:player_client=android", "-f", "bestaudio/best", 
         "-o", os.path.join(temp_dir, "cmd2.%(ext)s"), url],
         
        # Minimal command
        ["yt-dlp", "--no-check-certificate", "--geo-bypass", "--skip-download", "-f", "worst",
         "-o", os.path.join(temp_dir, "cmd3.%(ext)s"), url]
    ]
    
    for i, cmd in enumerate(command_sets):
        logger.info(f"Trying command set {i+1}: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Command set {i+1} successful")
                return True
            else:
                logger.warning(f"Command set {i+1} failed with code {result.returncode}")
                logger.warning(f"Error: {result.stderr}")
        except Exception as e:
            logger.warning(f"Command set {i+1} exception: {str(e)}")
    
    logger.error("All yt-dlp commands failed")
    return False

def test_youtube_dl_command(url, temp_dir):
    """Test downloading with youtube-dl command line."""
    logger.info("Testing youtube-dl command line...")
    
    # Check if youtube-dl is installed
    try:
        subprocess.run(["youtube-dl", "--version"], capture_output=True, text=True, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("youtube-dl not installed or not found")
        return False
    
    # Try youtube-dl command
    cmd = ["youtube-dl", "--no-check-certificate", "--geo-bypass", "-f", "bestaudio/best", 
           "-o", os.path.join(temp_dir, "ytdl.%(ext)s"), url]
    
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("youtube-dl command successful")
            return True
        else:
            logger.warning(f"youtube-dl command failed with code {result.returncode}")
            logger.warning(f"Error: {result.stderr}")
            return False
    except Exception as e:
        logger.warning(f"youtube-dl command exception: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Test YouTube download methods")
    parser.add_argument("url", help="YouTube video URL to test")
    parser.add_argument("--output-dir", "-o", help="Output directory for test files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Extract video ID from URL
    video_id = None
    if "v=" in args.url:
        video_id = args.url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in args.url:
        video_id = args.url.split("youtu.be/")[1].split("?")[0]
    
    if not video_id:
        logger.error("Could not extract video ID from URL")
        return 1
    
    logger.info(f"Starting YouTube download tests for video ID: {video_id}")
    logger.info(f"URL: {args.url}")
    
    # Create temp directory if output dir not specified
    temp_dir = None
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        temp_dir = args.output_dir
    else:
        temp_dir = tempfile.mkdtemp(prefix="youtube-test-")
    
    logger.info(f"Using output directory: {temp_dir}")
    
    # Configure SSL
    configure_ssl()
    
    # Run tests
    results = {
        "url_access": test_url_access(args.url),
        "video_info": get_video_info(video_id),
        "yt_dlp_python": test_yt_dlp_python(args.url, temp_dir),
        "yt_dlp_command": test_yt_dlp_command(args.url, temp_dir),
        "youtube_dl_command": test_youtube_dl_command(args.url, temp_dir)
    }
    
    # Print summary
    logger.info("\n--- TEST RESULTS SUMMARY ---")
    for test, result in results.items():
        status = "PASS" if result else "FAIL"
        logger.info(f"{test:20}: {status}")
    
    # Overall result
    if any(results.values()):
        logger.info("\nAt least one test passed. Try using the successful method in your application.")
        return 0
    else:
        logger.error("\nAll tests failed. This video may not be downloadable.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
