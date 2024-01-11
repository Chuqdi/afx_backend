#!/bin/bash

# Set the Docker image name and tag
IMAGE_NAME="afx-backend"
IMAGE_TAG="latest"

# Build the Docker image from the Dockerfile
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .

# Stop and remove existing container
if docker ps -a --format '{{.Names}}' | grep -q "^${IMAGE_NAME}\$"; then
    docker stop "${IMAGE_NAME}"
    docker rm -f "${IMAGE_NAME}"
fi

# Run the Docker container
docker run -d -p 8000:8000 --name ${IMAGE_NAME} "${IMAGE_NAME}:${IMAGE_TAG}"


# Display container information
docker ps --format "ID: {{.ID}}, Name: {{.Names}}, Image: {{.Image}}, Port(s): {{.Ports}}"
