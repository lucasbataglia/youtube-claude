#!/bin/bash
# Test script for YouTube Transcription and Download API

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
API_URL="http://localhost:5000"
ACTION="both"
OUTPUT_FILE="download.mp3"
YOUTUBE_URL=""

# Function to display usage
function show_usage {
    echo "Usage: $0 [options] -u YOUTUBE_URL"
    echo ""
    echo "Options:"
    echo "  -u, --url URL        YouTube video URL (required)"
    echo "  -a, --action ACTION  Action to perform: transcribe, download, both (default: both)"
    echo "  -o, --output FILE    Output file for MP3 download (default: download.mp3)"
    echo "  -s, --server URL     API server URL (default: http://localhost:5000)"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -u https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    echo "  $0 -a transcribe -u https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    echo "  $0 -a download -o my_song.mp3 -u https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -u|--url)
            YOUTUBE_URL="$2"
            shift
            shift
            ;;
        -a|--action)
            ACTION="$2"
            shift
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift
            shift
            ;;
        -s|--server)
            API_URL="$2"
            shift
            shift
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_usage
            ;;
    esac
done

# Check if YouTube URL is provided
if [ -z "$YOUTUBE_URL" ]; then
    echo -e "${RED}Error: YouTube URL is required${NC}"
    show_usage
fi

# Check if action is valid
if [[ "$ACTION" != "transcribe" && "$ACTION" != "download" && "$ACTION" != "both" ]]; then
    echo -e "${RED}Error: Invalid action: $ACTION${NC}"
    show_usage
fi

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is not installed. Please install curl and try again.${NC}"
    exit 1
fi

# Function to transcribe a video
function transcribe_video {
    echo -e "${YELLOW}Transcribing video: $YOUTUBE_URL${NC}"
    echo -e "${YELLOW}This may take a few minutes...${NC}"
    
    # Make API request
    response=$(curl -s -X POST "$API_URL/transcribe" \
        -H "Content-Type: application/json" \
        -d "{\"url\": \"$YOUTUBE_URL\"}")
    
    # Check if response contains an error
    if echo "$response" | grep -q "error"; then
        error=$(echo "$response" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
        echo -e "${RED}Error: $error${NC}"
        return 1
    fi
    
    # Extract transcription
    transcription=$(echo "$response" | grep -o '"transcription":"[^"]*"' | cut -d'"' -f4)
    
    # Print transcription
    echo -e "${GREEN}Transcription:${NC}"
    echo "$transcription"
    
    return 0
}

# Function to download a video as MP3
function download_video {
    echo -e "${YELLOW}Downloading video as MP3: $YOUTUBE_URL${NC}"
    echo -e "${YELLOW}Output file: $OUTPUT_FILE${NC}"
    
    # Make API request
    curl -s -o "$OUTPUT_FILE" "$API_URL/downloads?url=$YOUTUBE_URL"
    
    # Check if download was successful
    if [ $? -eq 0 ] && [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
        echo -e "${GREEN}Download completed: $OUTPUT_FILE${NC}"
        return 0
    else
        echo -e "${RED}Error: Failed to download video${NC}"
        return 1
    fi
}

# Perform the requested action
case $ACTION in
    transcribe)
        transcribe_video
        ;;
    download)
        download_video
        ;;
    both)
        transcribe_video
        echo ""
        download_video
        ;;
esac
