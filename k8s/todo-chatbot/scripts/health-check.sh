#!/bin/bash

# Script to check the health of deployed Todo Chatbot application
set -e

echo "Checking health of Todo Chatbot application..."

# Check if namespace exists
NAMESPACE_STATUS=$(kubectl get namespace todo-chatbot --no-headers -o custom-columns=STATUS:.status.phase 2>/dev/null || echo "NotFound")
if [ "$NAMESPACE_STATUS" != "Active" ]; then
    echo "❌ Namespace 'todo-chatbot' not found or not active"
    exit 1
else
    echo "✅ Namespace 'todo-chatbot' is active"
fi

# Check deployments
BACKEND_DEPLOYMENT=$(kubectl get deployment todo-chatbot-backend -n todo-chatbot --no-headers -o custom-columns=NAME:.metadata.name 2>/dev/null || echo "NotFound")
if [ "$BACKEND_DEPLOYMENT" = "NotFound" ]; then
    echo "❌ Backend deployment not found"
    exit 1
else
    echo "✅ Backend deployment exists"
fi

FRONTEND_DEPLOYMENT=$(kubectl get deployment todo-chatbot-frontend -n todo-chatbot --no-headers -o custom-columns=NAME:.metadata.name 2>/dev/null || echo "NotFound")
if [ "$FRONTEND_DEPLOYMENT" = "NotFound" ]; then
    echo "❌ Frontend deployment not found"
    exit 1
else
    echo "✅ Frontend deployment exists"
fi

# Check if deployments are ready
BACKEND_REPLICAS=$(kubectl get deployment todo-chatbot-backend -n todo-chatbot -o jsonpath='{.status.readyReplicas}')
BACKEND_DESIRED=$(kubectl get deployment todo-chatbot-backend -n todo-chatbot -o jsonpath='{.spec.replicas}')

FRONTEND_REPLICAS=$(kubectl get deployment todo-chatbot-frontend -n todo-chatbot -o jsonpath='{.status.readyReplicas}')
FRONTEND_DESIRED=$(kubectl get deployment todo-chatbot-frontend -n todo-chatbot -o jsonpath='{.spec.replicas}')

if [ "$BACKEND_REPLICAS" = "$BACKEND_DESIRED" ] && [ "$FRONTEND_REPLICAS" = "$FRONTEND_DESIRED" ]; then
    echo "✅ All pods are ready ($FRONTEND_REPLICAS/$FRONTEND_DESIRED frontend, $BACKEND_REPLICAS/$BACKEND_DESIRED backend)"
else
    echo "⚠️  Some pods are not ready (frontend: $FRONTEND_REPLICAS/$FRONTEND_DESIRED, backend: $BACKEND_REPLICAS/$BACKEND_DESIRED)"
fi

# Check services
BACKEND_SERVICE=$(kubectl get service todo-chatbot-backend -n todo-chatbot --no-headers -o custom-columns=NAME:.metadata.name 2>/dev/null || echo "NotFound")
if [ "$BACKEND_SERVICE" = "NotFound" ]; then
    echo "❌ Backend service not found"
    exit 1
else
    echo "✅ Backend service exists"
fi

FRONTEND_SERVICE=$(kubectl get service todo-chatbot-frontend -n todo-chatbot --no-headers -o custom-columns=NAME:.metadata.name 2>/dev/null || echo "NotFound")
if [ "$FRONTEND_SERVICE" = "NotFound" ]; then
    echo "❌ Frontend service not found"
    exit 1
else
    echo "✅ Frontend service exists"
fi

# Check ingress
INGRESS=$(kubectl get ingress todo-chatbot-ingress -n todo-chatbot --no-headers -o custom-columns=NAME:.metadata.name 2>/dev/null || echo "NotFound")
if [ "$INGRESS" = "NotFound" ]; then
    echo "❌ Ingress not found"
    exit 1
else
    echo "✅ Ingress exists"
fi

# Get pod statuses
echo ""
echo "Pod Statuses:"
kubectl get pods -n todo-chatbot

echo ""
echo "Service Statuses:"
kubectl get svc -n todo-chatbot

echo ""
echo "Deployment Statuses:"
kubectl get deployments -n todo-chatbot

echo ""
echo "Todo Chatbot application health check completed!"