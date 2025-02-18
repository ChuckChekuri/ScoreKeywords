#!/bin/bash

# Exit on error
set -e

COMPOSE_FILE=".devcontainer/docker-compose.yml"
BUILD_FILE=".devcontainer/docker-compose.build.yml"
CONTAINER_NAME="skw-app"

# Display help message
show_help() {
    echo "Usage: ./dev.sh [command] [options]"
    echo "Commands:"
    echo "  build    - Clean, rebuild and start containers"
    echo "  up       - Start existing containers"
    echo "Options:"
    echo "  --test   - Include test profile (Redis)"
    exit 0
}

# Function to cleanup existing containers and images
cleanup() {
    echo "Cleaning up existing containers and images..."
    # Stop and remove containers
    docker compose -f $COMPOSE_FILE -f $BUILD_FILE down --remove-orphans
    
    # Remove existing images
    local images=(
        "skw-image"
    )
    
    for img in "${images[@]}"; do
        if docker images | grep -q "$img"; then
            echo "Removing image: $img"
            docker rmi -f $(docker images | grep "$img" | awk '{print $3}')
        fi
    done
}

# Check if docker compose files exist
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Error: $COMPOSE_FILE not found"
    exit 1
fi

# Parse command line arguments
COMMAND=$1
PROFILE_ARG=""
if [ "$2" == "--test" ]; then
    PROFILE_ARG="--profile testing"
fi

case $COMMAND in
    "build")
        if [ ! -f "$BUILD_FILE" ]; then
            echo "Error: $BUILD_FILE not found"
            exit 1
        fi
        
        # Perform cleanup before building
        cleanup
        
        # Check for Dev Containers extension
        if ! code --list-extensions | grep -q "ms-vscode-remote.remote-containers"; then
            echo "Installing Dev Containers extension..."
            code --install-extension ms-vscode-remote.remote-containers
        fi
        
        docker compose -f $COMPOSE_FILE \
                      -f $BUILD_FILE \
                      $PROFILE_ARG \
                      up -d --build
                      
        # Wait for container to be ready
        echo "Waiting for container to initialize.."
        
        ;;
    "up")
        if ! docker container ls -a | grep $CONTAINER_NAME > /dev/null; then
            echo "Error: Container $CONTAINER_NAME not found. Run with 'build' first."
            exit 1
        fi
        docker compose -f $COMPOSE_FILE $PROFILE_ARG up -d --no-build
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    "")
        echo "Error: Command required"
        show_help
        ;;
    *)
        echo "Error: Unknown command '$COMMAND'"
        show_help
        ;;
esac