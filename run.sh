#!/bin/bash
# Run script for YouTube Transcription and Download API

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
PORT=5000
WORKERS=4
TIMEOUT=120
LOG_LEVEL="info"
MODE="development"

# Function to display usage
function show_usage {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -p, --port PORT      Port to run the server on (default: 5000)"
    echo "  -w, --workers N      Number of worker processes (default: 4)"
    echo "  -t, --timeout SEC    Worker timeout in seconds (default: 120)"
    echo "  -l, --log-level LVL  Log level: debug, info, warning, error, critical (default: info)"
    echo "  -m, --mode MODE      Run mode: development, production (default: development)"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                   # Run with default settings"
    echo "  $0 -p 8080 -w 2      # Run on port 8080 with 2 workers"
    echo "  $0 -m production     # Run in production mode"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--port)
            PORT="$2"
            shift
            shift
            ;;
        -w|--workers)
            WORKERS="$2"
            shift
            shift
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift
            shift
            ;;
        -l|--log-level)
            LOG_LEVEL="$2"
            shift
            shift
            ;;
        -m|--mode)
            MODE="$2"
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

# Check if Python virtual environment exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Check if Gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo -e "${RED}Gunicorn is not installed. Installing...${NC}"
    pip install gunicorn
fi

# Set environment variables based on mode
if [ "$MODE" == "production" ]; then
    export FLASK_ENV=production
    export FLASK_DEBUG=0
    echo -e "${YELLOW}Running in PRODUCTION mode${NC}"
else
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    echo -e "${YELLOW}Running in DEVELOPMENT mode${NC}"
fi

# Export port
export PORT=$PORT

# Create temp directory if it doesn't exist
mkdir -p temp

echo -e "${GREEN}Starting YouTube Transcription and Download API on port $PORT with $WORKERS workers...${NC}"

# Run with Gunicorn
gunicorn --workers=$WORKERS \
         --timeout=$TIMEOUT \
         --bind=0.0.0.0:$PORT \
         --log-level=$LOG_LEVEL \
         app:app
