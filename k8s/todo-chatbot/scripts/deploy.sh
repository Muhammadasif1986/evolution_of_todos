#!/bin/bash

# Script to deploy Todo Chatbot application to Kubernetes
set -e

echo "Deploying Todo Chatbot application to Kubernetes..."

# Apply namespace
echo "Creating namespace..."
kubectl apply -f k8s/todo-chatbot/manifests/namespace.yaml

# Apply deployments
echo "Deploying applications..."
kubectl apply -f k8s/todo-chatbot/manifests/deployment-backend.yaml
kubectl apply -f k8s/todo-chatbot/manifests/deployment-frontend.yaml

# Apply services
echo "Creating services..."
kubectl apply -f k8s/todo-chatbot/manifests/service-backend.yaml
kubectl apply -f k8s/todo-chatbot/manifests/service-frontend.yaml

# Apply ingress
echo "Creating ingress..."
kubectl apply -f k8s/todo-chatbot/manifests/ingress.yaml

echo "Todo Chatbot application deployed successfully!"
echo "Waiting for pods to be ready..."

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=todo-chatbot-backend -n todo-chatbot --timeout=180s
kubectl wait --for=condition=ready pod -l app=todo-chatbot-frontend -n todo-chatbot --timeout=180s

echo "Applications are running and ready!"