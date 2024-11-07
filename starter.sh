#!/bin/bash

# Define the image name
IMAGE_NAME="fetch-flask-app"

# Step 1: Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Step 2: Run the Docker container
echo "Running Docker container..."
docker run -d -p 8080:8080 $IMAGE_NAME

echo "Flask app is now running at http://localhost:8080"