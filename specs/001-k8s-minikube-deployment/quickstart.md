# Quickstart Guide: Kubernetes Minikube Deployment for Todo Chatbot

## Prerequisites

- Docker Desktop with Gordon AI (if available in your region)
- Minikube
- kubectl
- Helm
- kubectl-ai (optional, for AI-assisted operations)
- Kagent (optional, for AI-assisted operations)

## Setup Instructions

### 1. Start Minikube Cluster

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

# Build frontend image
docker build -f k8s/todo-chatbot/docker/frontend.Dockerfile -t todo-chatbot/frontend:latest .

# Build backend image
docker build -f k8s/todo-chatbot/docker/backend.Dockerfile -t todo-chatbot/backend:latest .
```

### 3. Deploy with Helm

```bash
# Navigate to the Helm chart directory
cd k8s/todo-chatbot/helm-chart

# Install the Todo Chatbot application
helm install todo-chatbot . --namespace todo-chatbot --create-namespace

# Verify deployment
kubectl get pods,svc,ingress -n todo-chatbot
```

### 4. Access the Application

```bash
# Get the Minikube IP
minikube ip

# Add entry to hosts file (on Linux/Mac)
echo "$(minikube ip) todo-chatbot.local" | sudo tee -a /etc/hosts

# On Windows (as Administrator in Command Prompt):
echo $(minikube ip) todo-chatbot.local >> C:\Windows\System32\drivers\etc\hosts
```

Visit `http://todo-chatbot.local` in your browser to access the Todo Chatbot application.

### 5. Using AI-Assisted Tools (Optional)

```bash
# Using kubectl-ai for operations
kubectl-ai "show me the status of pods in todo-chatbot namespace"
kubectl-ai "scale the frontend deployment to 3 replicas"
kubectl-ai "describe why the backend pod is failing"

# Using Kagent for cluster analysis
kagent "analyze the todo-chatbot namespace"
kagent "show resource utilization"
```

## Verification

Verify that all components are running correctly:

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

## Troubleshooting

1. **Application not accessible via ingress**: Ensure you've added the Minikube IP to your hosts file as shown above.

2. **Images not found**: Ensure you've run `eval $(minikube docker-env)` before building images.

3. **Insufficient resources**: Increase Minikube resources with `minikube delete` followed by `minikube start --cpus=4 --memory=8192`.

4. **Health check failures**: Check application logs with `kubectl logs` to identify startup issues.

## Cleanup

To remove the Todo Chatbot deployment:

```bash
# Uninstall the Helm release
helm uninstall todo-chatbot --namespace todo-chatbot

# Delete the namespace
kubectl delete namespace todo-chatbot

# Stop Minikube
minikube stop
```