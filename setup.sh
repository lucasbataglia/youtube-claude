#!/bin/bash
# Setup script for YouTube Transcription and Download API

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up YouTube Transcription and Download API...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 is not installed. Please install pip3 and try again.${NC}"
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}ffmpeg is not installed. It's required for audio processing.${NC}"
    echo -e "${YELLOW}Please install ffmpeg:${NC}"
    echo "  - On Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  - On macOS: brew install ffmpeg"
    echo "  - On Windows: Download from https://ffmpeg.org/download.html"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. You may want to edit it to customize settings.${NC}"
fi

# Create temp directory
echo -e "${YELLOW}Creating temp directory...${NC}"
mkdir -p temp

echo -e "${GREEN}Setup completed successfully!${NC}"
echo ""
echo -e "${YELLOW}To run the API:${NC}"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the API:"
echo "   python app.py"
echo ""
echo -e "${YELLOW}To run with Docker:${NC}"
echo "   docker-compose up -d"
echo ""
echo -e "${YELLOW}To test the API:${NC}"
echo "   python test.py --url \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\""
echo ""
echo -e "${GREEN}Enjoy using the YouTube Transcription and Download API!${NC}"
