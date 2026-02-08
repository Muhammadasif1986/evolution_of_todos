# Data Model: Kubernetes Resources for Todo Chatbot

## Kubernetes Resources

### Namespace
- **kind**: Namespace
- **name**: todo-chatbot
- **description**: Isolated environment for the Todo Chatbot application in Kubernetes

### Backend Deployment
- **kind**: Deployment
- **name**: todo-chatbot-backend
- **namespace**: todo-chatbot
- **replicas**: configurable (default: 1)
- **containers**:
  - **name**: backend
  - **image**: todo-chatbot/backend:latest
  - **ports**:
    - containerPort: 8000
    - protocol: TCP
  - **envFrom**:
    - secretRef: backend-secrets
    - configMapRef: backend-config
  - **resources**:
    - requests:
      - cpu: "100m"
      - memory: "128Mi"
    - limits:
      - cpu: "500m"
      - memory: "256Mi"
  - **livenessProbe**:
    - httpGet:
      - path: /health
      - port: 8000
    - initialDelaySeconds: 30
    - periodSeconds: 10
  - **readinessProbe**:
    - httpGet:
      - path: /ready
      - port: 8000
    - initialDelaySeconds: 5
    - periodSeconds: 5

### Frontend Deployment
- **kind**: Deployment
- **name**: todo-chatbot-frontend
- **namespace**: todo-chatbot
- **replicas**: configurable (default: 1)
- **containers**:
  - **name**: frontend
  - **image**: todo-chatbot/frontend:latest
  - **ports**:
    - containerPort: 3000
    - protocol: TCP
  - **env**:
    - name: BACKEND_URL
    - value: "http://todo-chatbot-backend.todo-chatbot.svc.cluster.local:8000"
  - **resources**:
    - requests:
      - cpu: "50m"
      - memory: "64Mi"
    - limits:
      - cpu: "200m"
      - memory: "128Mi"
  - **livenessProbe**:
    - httpGet:
      - path: /
      - port: 3000
    - initialDelaySeconds: 20
    - periodSeconds: 10
  - **readinessProbe**:
    - httpGet:
      - path: /
      - port: 3000
    - initialDelaySeconds: 5
    - periodSeconds: 5

### Backend Service
- **kind**: Service
- **name**: todo-chatbot-backend
- **namespace**: todo-chatbot
- **type**: ClusterIP
- **selector**: app=todo-chatbot-backend
- **ports**:
  - port: 8000
  - targetPort: 8000
  - protocol: TCP

### Frontend Service
- **kind**: Service
- **name**: todo-chatbot-frontend
- **namespace**: todo-chatbot
- **type**: ClusterIP
- **selector**: app=todo-chatbot-frontend
- **ports**:
  - port: 80
  - targetPort: 3000
  - protocol: TCP

### Ingress
- **kind**: Ingress
- **name**: todo-chatbot-ingress
- **namespace**: todo-chatbot
- **rules**:
  - host: todo-chatbot.local
  - http:
    - paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-chatbot-frontend
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: todo-chatbot-backend
            port:
              number: 80

### Backend ConfigMap
- **kind**: ConfigMap
- **name**: backend-config
- **namespace**: todo-chatbot
- **data**:
  - DATABASE_URL: postgresql://postgres:password@postgres-service:5432/todo_db
  - LOG_LEVEL: INFO
  - API_PREFIX: /api

### Backend Secret
- **kind**: Secret
- **name**: backend-secrets
- **namespace**: todo-chatbot
- **data**:
  - DB_PASSWORD: [base64 encoded password]
  - JWT_SECRET: [base64 encoded secret]

### PersistentVolumeClaim (if needed)
- **kind**: PersistentVolumeClaim
- **name**: todo-chatbot-storage
- **namespace**: todo-chatbot
- **accessModes**:
  - ReadWriteOnce
- **resources**:
  - requests:
    - storage: 1Gi