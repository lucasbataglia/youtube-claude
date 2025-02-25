import os
import tempfile
import uuid
import time
import logging
import ssl
import certifi
from flask import Flask, request, jsonify, send_file, render_template, make_response
from flask_cors import CORS
import yt_dlp
import whisper  # This is now openai-whisper
import numpy as np
import torch
from dotenv import load_dotenv

# Disable SSL verification globally (not recommended for production, but helps with SSL issues)
ssl._create_default_https_context = ssl._create_unverified_context

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Create a directory for storing temporary files
TEMP_DIR = os.environ.get("TEMP_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp"))
os.makedirs(TEMP_DIR, exist_ok=True)

# Load the actual Whisper model
model_size = os.environ.get("WHISPER_MODEL", "base")
logger.info(f"Loading Whisper model: {model_size}")

# Check if CUDA is available for GPU acceleration
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")

# Load the model
try:
    model = whisper.load_model(model_size, device=device)
    logger.info(f"Whisper model {model_size} loaded successfully")
except Exception as e:
    logger.error(f"Error loading Whisper model: {str(e)}", exc_info=True)
    raise

@app.route('/')
def index():
    """
    Render the web interface.
    """
    return render_template('index.html')

@app.route('/health')
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "whisper_model": model_size,
        "hostname": os.environ.get("HOSTNAME", "unknown")
    })

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    """
    Endpoint to transcribe a YouTube video.
    
    Expected JSON payload:
    {
        "url": "https://www.youtube.com/watch?v=VIDEO_ID"
    }
    """
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required"}), 400
    
    youtube_url = data['url']
    logger.info(f"Transcription request for URL: {youtube_url}")
    
    try:
        # Create a unique temporary directory for this request
        temp_dir = os.path.join(TEMP_DIR, str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Download audio from YouTube
            audio_path = download_audio(youtube_url, temp_dir)
            
            # Transcribe the audio using the Whisper model
            logger.info(f"Transcribing audio file: {audio_path}")
            result = model.transcribe(audio_path, fp16=False if device == "cpu" else True)
            
            # Clean up temporary files
            try:
                os.remove(audio_path)
                os.rmdir(temp_dir)
            except Exception as e:
                logger.warning(f"Error cleaning up temporary files: {str(e)}")
            
            return jsonify({
                "transcription": result["text"],
                "segments": result["segments"]
            })
        except Exception as e:
            # Clean up temporary directory if it exists
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
            
            # Re-raise the exception to be caught by the outer try-except
            raise e
    
    except Exception as e:
        logger.error(f"Error transcribing video: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/downloads', methods=['GET'])
def download_mp3():
    """
    Endpoint to download a YouTube video as MP3.
    
    Expected query parameters:
    url: The YouTube video URL
    """
    youtube_url = request.args.get('url')
    
    if not youtube_url:
        return jsonify({"error": "URL is required"}), 400
    
    logger.info(f"Download request for URL: {youtube_url}")
    
    try:
        # Create a unique temporary directory for this request
        temp_dir = os.path.join(TEMP_DIR, str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)
        
        # Download audio from YouTube
        audio_path = download_audio(youtube_url, temp_dir)
        
        # Get video title for filename
        video_id = youtube_url.split("v=")[-1].split("&")[0]
        filename = f"youtube_audio_{video_id}.mp3"
        
        # Send the file to the client
        response = make_response(send_file(
            audio_path,
            as_attachment=True,
            download_name=filename,
            mimetype="audio/mpeg"
        ))
        
        # Add headers to prevent caching
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        
        # Clean up temporary files after sending (this won't work as expected, but we'll handle it)
        # We'll need a background task or a cleanup job for production
        
        return response
    
    except Exception as e:
        logger.error(f"Error downloading audio: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

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
    
    try:
        # Create a custom opener that ignores SSL verification
        import urllib.request
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        urllib.request.install_opener(opener)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': False,  # Set to True in production, False for debugging
            'no_warnings': False,  # Set to False for debugging
            'ignoreerrors': False,
            'geo_bypass': True,
            'nocheckcertificate': True,  # Ignore SSL certificate verification
            'socket_timeout': 30,  # Increase timeout
            'verbose': True,  # Add verbose output for debugging
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Downloading audio from: {youtube_url}")
            ydl.download([youtube_url])
            
        # Check if the file was downloaded successfully
        if not os.path.exists(audio_path):
            raise Exception("Failed to download audio file")
            
        return audio_path
        
    except Exception as e:
        logger.error(f"Error downloading audio: {str(e)}", exc_info=True)
        # Instead of creating an invalid dummy file, raise the exception
        # so the calling function can handle it appropriately
        raise Exception(f"Failed to download audio from YouTube: {str(e)}")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host='0.0.0.0', port=port, debug=debug)
