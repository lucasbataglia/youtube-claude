#!/bin/bash
# Script to update and redeploy the YouTube API application

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
VPS_USER=""
VPS_HOST=""
IMAGE_NAME="youtube-api"
IMAGE_TAG="latest"
PORTAINER_STACK="youtube-api"

# Function to display usage
function show_usage {
    echo "Usage: $0 -u VPS_USER -h VPS_HOST [-i IMAGE_NAME] [-t IMAGE_TAG] [-s STACK_NAME]"
    echo ""
    echo "Options:"
    echo "  -u, --user USER       VPS username (required)"
    echo "  -h, --host HOST       VPS hostname or IP address (required)"
    echo "  -i, --image NAME      Docker image name (default: youtube-api)"
    echo "  -t, --tag TAG         Docker image tag (default: latest)"
    echo "  -s, --stack STACK     Portainer stack name (default: youtube-api)"
    echo "  --help                Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 -u admin -h example.com"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -u|--user)
            VPS_USER="$2"
            shift
            shift
            ;;
        -h|--host)
            VPS_HOST="$2"
            shift
            shift
            ;;
        -i|--image)
            IMAGE_NAME="$2"
            shift
            shift
            ;;
        -t|--tag)
            IMAGE_TAG="$2"
            shift
            shift
            ;;
        -s|--stack)
            PORTAINER_STACK="$2"
            shift
            shift
            ;;
        --help)
            show_usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_usage
            ;;
    esac
done

# Check if required parameters are provided
if [ -z "$VPS_USER" ] || [ -z "$VPS_HOST" ]; then
    echo -e "${RED}Error: VPS username and hostname are required${NC}"
    show_usage
fi

# Full image name with tag
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

echo -e "${YELLOW}Updating and redeploying YouTube API application...${NC}"

# Step 1: Build the Docker image locally
echo -e "${YELLOW}Building Docker image: ${FULL_IMAGE_NAME}...${NC}"
docker build -t ${FULL_IMAGE_NAME} .

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to build Docker image${NC}"
    exit 1
fi

# Step 2: Save the image to a tar file
echo -e "${YELLOW}Saving Docker image to a tar file...${NC}"
TAR_FILE="${IMAGE_NAME}.tar"
docker save -o ${TAR_FILE} ${FULL_IMAGE_NAME}

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to save Docker image${NC}"
    exit 1
fi

# Step 3: Copy the image to the VPS
echo -e "${YELLOW}Copying Docker image to VPS: ${VPS_USER}@${VPS_HOST}...${NC}"
scp ${TAR_FILE} ${VPS_USER}@${VPS_HOST}:~/${TAR_FILE}

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to copy Docker image to VPS${NC}"
    exit 1
fi

# Step 4: Load the image on the VPS and update the stack
echo -e "${YELLOW}Loading Docker image on VPS and updating stack...${NC}"
ssh ${VPS_USER}@${VPS_HOST} << EOF
    # Load the Docker image
    echo "Loading Docker image..."
    docker load -i ~/${TAR_FILE}
    
    # Remove the tar file
    echo "Removing tar file..."
    rm ~/${TAR_FILE}
    
    # Update the stack in Portainer
    echo "Updating Portainer stack..."
    # This assumes you have the Portainer CLI or API access configured
    # You may need to adjust this command based on your Portainer setup
    docker stack deploy -c ~/stacks/${PORTAINER_STACK} ${PORTAINER_STACK} --with-registry-auth
    
    echo "Deployment completed!"
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to update stack on VPS${NC}"
    exit 1
fi

# Clean up local tar file
echo -e "${YELLOW}Cleaning up local tar file...${NC}"
rm ${TAR_FILE}

echo -e "${GREEN}YouTube API application has been successfully updated and redeployed!${NC}"
echo -e "${YELLOW}Note: You may need to manually restart the service in Portainer if it doesn't automatically update.${NC}"
