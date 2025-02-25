#!/usr/bin/env python3
"""
Test script for downloading YouTube videos using pytube.
"""

import os
import sys
import tempfile
import subprocess
from pytube import YouTube

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_pytube.py <youtube_url>")
        return 1
    
    youtube_url = sys.argv[1]
    print(f"Testing pytube download for: {youtube_url}")
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix="pytube-test-")
    print(f"Using temp directory: {temp_dir}")
    
    try:
        # Create YouTube object
        yt = YouTube(youtube_url)
        
        # Print video info
        print(f"Title: {yt.title}")
        print(f"Author: {yt.author}")
        print(f"Length: {yt.length} seconds")
        
        # Get audio stream
        print("Getting audio stream...")
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            print("No audio stream found")
            return 1
        
        print(f"Audio stream: {audio_stream}")
        
        # Download audio
        print("Downloading audio...")
        audio_file = audio_stream.download(output_path=temp_dir)
        print(f"Downloaded to: {audio_file}")
        
        # Convert to mp3 using ffmpeg if available
        try:
            mp3_file = os.path.splitext(audio_file)[0] + ".mp3"
            print(f"Converting to MP3: {mp3_file}")
            
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", audio_file,
                "-vn",
                "-ar", "44100",
                "-ac", "2",
                "-b:a", "192k",
                "-f", "mp3",
                mp3_file
            ]
            
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            print(f"Converted to MP3: {mp3_file}")
            
            # Remove original file
            os.remove(audio_file)
            
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"Failed to convert to MP3: {e}")
            print("Using original file instead")
            mp3_file = audio_file
        
        print(f"Final audio file: {mp3_file}")
        print(f"File size: {os.path.getsize(mp3_file) / (1024 * 1024):.2f} MB")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
