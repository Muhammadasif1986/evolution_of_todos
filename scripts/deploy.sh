#!/bin/bash

# Deployment script for Full-Stack Todo Web Application

echo "Deploying Full-Stack Todo Web Application..."

# Check if docker-compose is available
if ! [ -x "$(command -v docker-compose)" ]; then
  echo "Error: docker-compose is not installed." >&2
  exit 1
fi

# Navigate to docker directory and deploy
cd docker

echo "Building and starting services..."
docker-compose up --build -d

echo "Deployment complete!"
echo "Frontend should be available at http://localhost:3000"
echo "Backend API should be available at http://localhost:8000"
echo "Health check: http://localhost:8000/health"