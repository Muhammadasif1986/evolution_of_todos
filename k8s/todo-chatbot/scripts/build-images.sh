#!/bin/bash

# Script to build Docker images for Todo Chatbot application
set -e

echo "Building Docker images for Todo Chatbot..."

# Build frontend image
echo "Building frontend image..."
docker build -f k8s/todo-chatbot/docker/frontend.Dockerfile -t todo-chatbot/frontend:latest .

# Build backend image
echo "Building backend image..."
docker build -f k8s/todo-chatbot/docker/backend.Dockerfile -t todo-chatbot/backend:latest .

echo "Docker images built successfully!"
echo "Frontend image: todo-chatbot/frontend:latest"
echo "Backend image: todo-chatbot/backend:latest"