#!/bin/bash

# Exit on error
set -e

COMPOSE_FILE=".devcontainer/docker-compose.yml"
BUILD_FILE=".devcontainer/docker-compose.build.yml"
CONTAINER_NAME="score-keywords-app"

# Display help message
show_help() {
    echo "Usage: ./dev.sh [command] [options]"
    echo "Commands:"
    echo "  build    - Build and start containers"
    echo "  up       - Start existing containers"
    echo "Options:"
    echo "  --test   - Include test profile (Redis)"
    exit 0
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
        docker compose -f $COMPOSE_FILE \
                      -f $BUILD_FILE \
                      $PROFILE_ARG \
                      up -d --build
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