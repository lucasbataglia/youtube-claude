#!/usr/bin/env python3
"""
Test script for the YouTube Transcription and Download API.
This script demonstrates how to use the API programmatically.
"""

import requests
import json
import os
import argparse

def transcribe_video(url, api_url="http://localhost:5000"):
    """
    Transcribe a YouTube video.
    
    Args:
        url: YouTube video URL
        api_url: API base URL
        
    Returns:
        Transcription result
    """
    endpoint = f"{api_url}/transcribe"
    payload = {"url": url}
    headers = {"Content-Type": "application/json"}
    
    print(f"Transcribing video: {url}")
    response = requests.post(endpoint, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def download_mp3(url, output_file="download.mp3", api_url="http://localhost:5000"):
    """
    Download a YouTube video as MP3.
    
    Args:
        url: YouTube video URL
        output_file: Output file path
        api_url: API base URL
        
    Returns:
        True if successful, False otherwise
    """
    endpoint = f"{api_url}/downloads"
    params = {"url": url}
    
    print(f"Downloading video as MP3: {url}")
    response = requests.get(endpoint, params=params, stream=True)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded to: {output_file}")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def main():
    parser = argparse.ArgumentParser(description="Test the YouTube Transcription and Download API")
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--api", default="http://localhost:5000", help="API base URL")
    parser.add_argument("--action", choices=["transcribe", "download", "both"], default="both", 
                        help="Action to perform")
    parser.add_argument("--output", default="download.mp3", help="Output file for MP3 download")
    
    args = parser.parse_args()
    
    if args.action in ["transcribe", "both"]:
        result = transcribe_video(args.url, args.api)
        if result:
            print("\nTranscription:")
            print(result["transcription"])
            print("\nSegments:")
            for segment in result["segments"][:3]:  # Show first 3 segments
                print(f"{segment['start']:.2f}s - {segment['end']:.2f}s: {segment['text']}")
            if len(result["segments"]) > 3:
                print("...")
    
    if args.action in ["download", "both"]:
        download_mp3(args.url, args.output, args.api)

if __name__ == "__main__":
    main()
