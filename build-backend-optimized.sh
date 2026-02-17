#!/bin/bash

# Optimized build script for todo-chatbot backend
set -e

echo "Building optimized todo-chatbot backend image..."

# Use buildx for better caching and multi-platform support
docker buildx build \
  --platform linux/amd64 \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from type=local,src=/tmp/.buildx-cache \
  --cache-to type=local,dest=/tmp/.buildx-cache-new \
  -t todo-chatbot/backend:optimized \
  -f k8s/todo-chatbot/docker/backend.Dockerfile.optimized \
  .

# Move the new cache to replace the old one
if [ -d "/tmp/.buildx-cache-new" ]; then
  rm -rf /tmp/.buildx-cache
  mv /tmp/.buildx-cache-new /tmp/.buildx-cache
fi

echo "Build completed successfully!"