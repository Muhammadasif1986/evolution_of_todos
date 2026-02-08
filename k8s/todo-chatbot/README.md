# Todo Chatbot Kubernetes Deployment

This directory contains all the necessary files to deploy the Todo Chatbot application to a Kubernetes cluster using Minikube.

## Prerequisites

- Docker (with Docker AI Agent - Gordon - if available in your region)
- Minikube
- kubectl
- Helm
- kubectl-ai (optional, for AI-assisted operations)
- Kagent (optional, for AI-assisted operations)

## Directory Structure

```
k8s/
└── todo-chatbot/
    ├── docker/
    │   ├── frontend.Dockerfile
    │   └── backend.Dockerfile
    ├── helm-chart/
    │   ├── Chart.yaml
    │   ├── values.yaml
    │   └── templates/
    │       ├── deployment-frontend.yaml
    │       ├── deployment-backend.yaml
    │       ├── service-frontend.yaml
    │       ├── service-backend.yaml
    │       ├── ingress.yaml
    │       ├── configmap.yaml
    │       ├── secret.yaml
    │       ├── serviceaccount.yaml
    │       └── _helpers.tpl
    ├── manifests/
    │   ├── namespace.yaml
    │   ├── deployment-frontend.yaml
    │   ├── deployment-backend.yaml
    │   ├── service-frontend.yaml
    │   ├── service-backend.yaml
    │   └── ingress.yaml
    ├── scripts/
    │   ├── build-images.sh
    │   ├── deploy.sh
    │   └── health-check.sh
    └── AI-ASSISTED-OPERATIONS.md
```

## Deployment Steps

### 1. Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192

# Enable ingress addon
minikube addons enable ingress

# Verify cluster is running
kubectl cluster-info
```

### 2. Build Docker Images

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Run the build script
./k8s/todo-chatbot/scripts/build-images.sh
```

**Note on Docker AI (Gordon):** If Docker AI Agent (Gordon) is available in your region, you can use it for Docker operations:
```bash
# Using Gordon for Docker operations (if available)
docker ai "create a Dockerfile for a Next.js application"
docker ai "create a Dockerfile for a FastAPI application"
docker ai "optimize the Dockerfile for smaller image size"
```

If Docker AI (Gordon) is unavailable in your region, the Dockerfiles were generated using Claude Code as specified in the requirements.

### 3. Deploy with Kubernetes Manifests

```bash
# Run the deployment script
./k8s/todo-chatbot/scripts/deploy.sh
```

### 4. Or Deploy with Helm

```bash
# Navigate to the Helm chart directory
cd k8s/todo-chatbot/helm-chart

# Install the Todo Chatbot application
helm install todo-chatbot . --namespace todo-chatbot --create-namespace

# Verify deployment
kubectl get pods,svc,ingress -n todo-chatbot
```

### 5. Access the Application

```bash
# Get the Minikube IP
minikube ip

# Add entry to hosts file (on Linux/Mac)
echo "$(minikube ip) todo-chatbot.local" | sudo tee -a /etc/hosts
```

Visit `http://todo-chatbot.local` in your browser to access the Todo Chatbot application.

## Verification

Check the health of your deployment:

```bash
./k8s/todo-chatbot/scripts/health-check.sh
```

Or manually verify:

```bash
# Check pod status
kubectl get pods -n todo-chatbot

# Check services
kubectl get svc -n todo-chatbot

# Check ingress
kubectl get ingress -n todo-chatbot

# Check logs for any issues
kubectl logs -l app=todo-chatbot-frontend -n todo-chatbot
kubectl logs -l app=todo-chatbot-backend -n todo-chatbot
```

## Using AI-Assisted Tools

### kubectl-ai for Intelligent Kubernetes Operations

```bash
# Using kubectl-ai for operations
kubectl-ai "show me the status of pods in todo-chatbot namespace"
kubectl-ai "scale the frontend deployment to 3 replicas"
kubectl-ai "describe why the backend pod is failing"
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to handle more load"
kubectl-ai "check why the pods are failing"
kubectl-ai "install the todo-chatbot helm chart from k8s/todo-chatbot/helm-chart"
kubectl-ai "verify all pods in todo-chatbot namespace are running"
```

### Kagent for Advanced Analysis

```bash
# Using Kagent for cluster analysis
kagent "analyze the cluster health"
kagent "optimize resource allocation"
kagent "analyze the todo-chatbot namespace"
kagent "show resource utilization"
```

For more detailed examples of AI-assisted operations, see [AI-ASSISTED-OPERATIONS.md](./AI-ASSISTED-OPERATIONS.md).

## Cleanup

To remove the Todo Chatbot deployment:

```bash
# Uninstall the Helm release (if deployed with Helm)
helm uninstall todo-chatbot --namespace todo-chatbot

# Or delete resources manually (if deployed with manifests)
kubectl delete -f k8s/todo-chatbot/manifests/ --all

# Delete the namespace
kubectl delete namespace todo-chatbot

# Stop Minikube
minikube stop
```