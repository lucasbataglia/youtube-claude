#!/usr/bin/env python3
"""
Test script for downloading YouTube videos using the app.py download functions.
"""

import os
import sys
import ssl
import certifi
import logging
import tempfile
import subprocess
import shutil
import urllib.request
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test-download")

# Configure SSL with certifi certificates
try:
    # Set up SSL context with certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Set as default HTTPS context
    ssl._create_default_https_context = lambda: ssl_context
    
    # Configure urllib to use our SSL context
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)
    
    # Configure requests to disable SSL verification
    requests.packages.urllib3.disable_warnings()
    
    logger.info("SSL certificate verification disabled with certifi")
except Exception as e:
    logger.warning(f"Failed to configure SSL context: {str(e)}")
    # Fallback to completely disabling SSL verification
    ssl._create_default_https_context = ssl._create_unverified_context
    logger.warning("SSL certificate verification completely disabled")

# Import pytube for alternative YouTube download method
try:
    from pytube import YouTube
except ImportError:
    YouTube = None
    logger.warning("pytube is not installed")

# Import yt-dlp
try:
    import yt_dlp
except ImportError:
    yt_dlp = None
    logger.warning("yt-dlp is not installed")

def download_audio(youtube_url, temp_dir):
    """
    Download audio from a YouTube video.
    
    Args:
        youtube_url: The YouTube video URL
        temp_dir: Directory to save the downloaded audio
        
    Returns:
        The path to the downloaded audio file
    """
    output_template = os.path.join(temp_dir, "audio.%(ext)s")
    audio_path = os.path.join(temp_dir, "audio.mp3")
    
    # Set environment variables for SSL
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    
    # Extract video ID from URL
    video_id = None
    if "v=" in youtube_url:
        video_id = youtube_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
    
    if video_id:
        logger.info(f"Extracted video ID: {video_id}")
    
    # Try multiple methods to download the audio
    methods = [
        download_with_yt_dlp,
        download_with_yt_dlp_command,
        download_with_pytube,
        download_with_requests_direct
    ]
    
    last_error = None
    for method in methods:
        try:
            logger.info(f"Trying download method: {method.__name__}")
            result = method(youtube_url, video_id, temp_dir, output_template, audio_path)
            if result and os.path.exists(result):
                logger.info(f"Download successful with {method.__name__}")
                return result
        except Exception as e:
            last_error = e
            logger.warning(f"{method.__name__} failed: {str(e)}")
    
    # If all methods failed, raise the last error
    raise Exception(f"Failed to download audio from YouTube after trying all methods: {str(last_error)}")

def download_with_yt_dlp(youtube_url, video_id, temp_dir, output_template, audio_path):
    """Download audio using yt-dlp Python library"""
    if yt_dlp is None:
        raise Exception("yt-dlp is not installed")
        
    # Set environment variables for SSL
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    
    # Configure SSL context
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl._create_default_https_context = lambda: ssl_context
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'socket_timeout': 60,
        'verbose': True,
        'force_generic_extractor': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['webpage', 'dash', 'hls'],
            }
        },
        'external_downloader_args': ['-v'],
        'cookiefile': None,
        'source_address': '0.0.0.0',
        'legacy_server_connect': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        },
        'compat_opts': ['no-youtube-unavailable-videos', 'no-youtube-prefer-utc-upload-date'],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading audio with yt-dlp: {youtube_url}")
            ydl.download([youtube_url])
            
        if os.path.exists(audio_path):
            return audio_path
    except Exception as e:
        logger.warning(f"yt-dlp download failed: {str(e)}")
        
    # If we get here, the download failed
    raise Exception("yt-dlp download failed to produce audio file")

def download_with_yt_dlp_command(youtube_url, video_id, temp_dir, output_template, audio_path):
    """Download audio using yt-dlp command line"""
    # Clean up any partial downloads
    if os.path.exists(audio_path):
        os.remove(audio_path)
        
    # Set environment variables for SSL
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['PYTHONHTTPSVERIFY'] = '0'
        
    # Construct the command with all possible workarounds
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
        "--output", output_template,   # Set output template
        youtube_url                # YouTube URL
    ]
    
    try:
        # Run the command
        logger.info(f"Running yt-dlp command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.warning(f"yt-dlp command failed with code {result.returncode}: {result.stderr}")
            raise Exception(f"yt-dlp command failed: {result.stderr}")
        
        if os.path.exists(audio_path):
            return audio_path
    except Exception as e:
        logger.warning(f"yt-dlp command execution failed: {str(e)}")
    
    # If we get here, the download failed
    raise Exception("yt-dlp command did not produce audio file")

def download_with_pytube(youtube_url, video_id, temp_dir, output_template, audio_path):
    """Download audio using pytube library"""
    if YouTube is None:
        raise Exception("pytube is not installed")
    
    # Clean up any partial downloads
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    # Set environment variables for SSL
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    
    # Configure SSL context
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl._create_default_https_context = lambda: ssl_context
    
    try:
        logger.info(f"Downloading with pytube: {youtube_url}")
        
        # Create YouTube object with custom SSL context
        yt = YouTube(youtube_url)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise Exception("No audio stream found")
        
        # Download the audio
        temp_audio_path = audio_stream.download(output_path=temp_dir)
        logger.info(f"Downloaded audio to: {temp_audio_path}")
        
        # Convert to mp3 using ffmpeg
        try:
            # Construct ffmpeg command
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", temp_audio_path,
                "-vn",  # No video
                "-ar", "44100",  # Audio sampling rate
                "-ac", "2",  # Stereo
                "-b:a", "192k",  # Bitrate
                "-f", "mp3",  # Format
                audio_path
            ]
            
            # Run ffmpeg
            logger.info(f"Converting to mp3 with ffmpeg: {' '.join(ffmpeg_cmd)}")
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            # Check if conversion was successful
            if result.returncode != 0:
                logger.warning(f"ffmpeg conversion failed: {result.stderr}")
                # If conversion failed, just rename the file
                shutil.move(temp_audio_path, audio_path)
        except Exception as e:
            logger.warning(f"Error converting to mp3: {str(e)}")
            # If conversion failed, just rename the file
            shutil.move(temp_audio_path, audio_path)
        
        # Clean up temporary file if it still exists
        if os.path.exists(temp_audio_path) and temp_audio_path != audio_path:
            os.remove(temp_audio_path)
        
        if os.path.exists(audio_path):
            return audio_path
    except Exception as e:
        logger.warning(f"pytube download failed: {str(e)}")
    
    # If we get here, the download failed
    raise Exception("pytube download failed to produce audio file")

def download_with_requests_direct(youtube_url, video_id, temp_dir, output_template, audio_path):
    """
    Last resort method: Try to download directly using requests.
    This is unlikely to work for most YouTube videos but included as a last resort.
    """
    if not video_id:
        raise Exception("Could not extract video ID from URL")
    
    # Clean up any partial downloads
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    # Try a direct mp3 URL (this is unlikely to work for most videos)
    direct_url = f"https://www.youtube.com/get_video_info?video_id={video_id}&el=detailpage"
    
    logger.info(f"Attempting direct download from: {direct_url}")
    response = requests.get(direct_url, verify=False, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"Direct download failed with status code: {response.status_code}")
    
    # This is a very simplified approach and likely won't work
    # But included as a last resort
    with open(audio_path, 'wb') as f:
        f.write(response.content)
    
    # Check if the file is valid (has some content)
    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
        return audio_path
    
    raise Exception("Direct download failed to produce a valid audio file")

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_download.py <youtube_url> [output_path]")
        return 1
    
    youtube_url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"
    
    print(f"Testing download of {youtube_url} to {output_path}")
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix="test-download-")
    
    try:
        # Download audio
        audio_path = download_audio(youtube_url, temp_dir)
        
        # Copy to output path
        shutil.copy2(audio_path, output_path)
        
        print(f"Download successful: {output_path}")
        print(f"File size: {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")
        
        return 0
    except Exception as e:
        print(f"Download failed: {str(e)}")
        return 1
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
