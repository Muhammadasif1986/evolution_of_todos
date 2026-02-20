# Quickstart Guide: Advanced Cloud Deployment

## Overview
This guide provides instructions for setting up and running the advanced todo chatbot with event-driven architecture using Kafka and Dapr integration.

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Minikube, AKS, GKE, or DigitalOcean)
- kubectl
- Dapr CLI
- Python 3.11+
- Node.js 18+

## Local Development Setup

### 1. Install Dapr
```bash
# Install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Initialize Dapr in standalone mode
dapr init

# Or initialize Dapr in Kubernetes
dapr init -k
```

### 2. Start Kafka/Redpanda locally
```bash
# Option 1: Use Redpanda (Kafka-compatible)
docker run -d --pull=always --name=redpanda-1 \
  --rm -p 9092:9092 -p 9644:9644 \
  docker.redpanda.com/redpandadata/redpanda:latest \
  redpanda start --mode dev-container --smp 1 --memory 1G --reserve-memory 100M --overprovisioned

# Option 2: Use Apache Kafka with Docker Compose
docker-compose -f docker-compose.kafka.yml up -d
```

### 3. Set up the Backend Service
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start the service with Dapr
dapr run --app-id todo-backend --app-port 8000 -- uvicorn src.api.main:app --reload
```

### 4. Set up the Frontend Service
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start the development server
npm run dev
```

## Kafka Topics Setup

The system requires the following Kafka topics to be created:

```bash
# Create required topics for the event-driven architecture
kafka-topics --create --topic task-events --bootstrap-server localhost:9092
kafka-topics --create --topic reminders --bootstrap-server localhost:9092
kafka-topics --create --topic task-updates --bootstrap-server localhost:9092
```

## Dapr Component Configuration

### Kafka Pub/Sub Component
Create the file `backend/config/dapr_components/pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "localhost:9092"
  - name: consumerGroup
    value: "todo-service"
  - name: authType
    value: "none"
```

### PostgreSQL State Store Component
Create the file `backend/config/dapr_components/statestore.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-state
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=localhost user=postgres password=postgres dbname=todo port=5432 sslmode=disable"
  - name: versionColumnType
    value: "version"
```

### Secrets Component
Create the file `backend/config/dapr_components/secrets.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: local-secret-store
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: "/path/to/secrets.json"
  - name: nestedSeparator
    value: ":"
```

Apply these configurations to your Kubernetes cluster:
```bash
kubectl apply -f backend/config/dapr_components/
```

## Kubernetes Deployment

### 1. Deploy Kafka/Redpanda to Kubernetes
```bash
# Install Redpanda to Kubernetes
kubectl create namespace kafka
kubectl apply -f kubernetes/kafka/kafka-cluster.yaml
```

### 2. Build and Push Docker Images
```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .
docker tag todo-backend:latest <your-registry>/todo-backend:latest
docker push <your-registry>/todo-backend:latest

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
docker tag todo-frontend:latest <your-registry>/todo-frontend:latest
docker push <your-registry>/todo-frontend:latest
```

### 3. Deploy to Kubernetes
```bash
# Install Helm chart
helm install todo-chatbot kubernetes/charts/todo-chatbot/ \
  --set backend.image.repository=<your-registry>/todo-backend \
  --set frontend.image.repository=<your-registry>/todo-frontend \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest
```

## Testing the System

### 1. Test Event-Driven Architecture
```bash
# Send a test task creation
curl -X POST http://localhost:3500/v1.0/invoke/todo-backend/method/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test recurring task",
    "description": "This is a test recurring task",
    "recurrence_pattern": {
      "type": "daily",
      "interval": 1
    }
  }'
```

### 2. Verify Kafka Events
```bash
# Consume events from Kafka to verify proper publishing
kafka-console-consumer --bootstrap-server localhost:9092 --topic task-events --from-beginning
```

### 3. Test Dapr Integration
```bash
# Test pub/sub functionality
curl -X POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events \
  -H "Content-Type: application/json" \
  -d '{"event_type": "test", "data": {"message": "Test event"}}'
```

## Key Configuration Values

### Environment Variables
- `DATABASE_URL`: Connection string for PostgreSQL database
- `KAFKA_BROKERS`: Comma-separated list of Kafka brokers (e.g., "localhost:9092")
- `DAPR_HTTP_ENDPOINT`: Dapr sidecar HTTP endpoint (default: http://localhost:3500)
- `DAPR_GRPC_ENDPOINT`: Dapr sidecar gRPC endpoint (default: http://localhost:50001)
- `NEON_DATABASE_URL`: Neon Serverless PostgreSQL connection string
- `OPENAI_API_KEY`: API key for OpenAI integration

## Troubleshooting

1. **Dapr sidecar not starting**: Ensure Dapr is properly initialized and the sidecar is injected in your deployment
2. **Kafka connection issues**: Verify that Kafka/Redpanda is running and accessible at the configured address
3. **Database connection failures**: Check that the PostgreSQL database is accessible and credentials are correct
4. **Event processing delays**: Monitor Kafka consumer lag and ensure sufficient consumer instances

## Next Steps

1. Implement the MCP server for chatbot integration
2. Deploy monitoring and logging infrastructure (Prometheus, Grafana, ELK stack)
3. Set up CI/CD pipeline for automated deployments
4. Configure security and authentication for production environments