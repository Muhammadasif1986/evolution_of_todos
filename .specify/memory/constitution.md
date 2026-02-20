<!--
Sync Impact Report:
Version change: 1.0.0 -> 1.1.0
Modified principles: Updated principles to include Kafka, Dapr, and advanced cloud features
Added sections: Event-Driven Architecture Requirements, Dapr Integration Standards, Advanced Features Requirements
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ Updated to reflect new principles
  - .specify/templates/spec-template.md: ✅ Updated to reflect new requirements
  - .specify/templates/tasks-template.md: ✅ Updated to reflect new requirements
  - .specify/templates/commands/*.md: ✅ Review completed for new requirements
Follow-up TODOs: None
-->
# Todo Spec-Driven Development Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development must follow the Spec-Kit Plus workflow: Specify → Plan → Tasks → Implement. No code may be written without a corresponding task derived from an approved specification. This ensures alignment between requirements and implementation, prevents "vibe coding," and maintains traceability from user needs to code artifacts.

### II. AI-Native Development
Leverage Claude Code and other AI agents as primary development tools. Human developers focus on system architecture, specification, and validation rather than syntax implementation. All code generation must be done through AI agents following the established workflow, with humans providing requirements and reviewing outputs.

### III. Progressive Evolution Architecture
Follow the 5-phase evolution approach: Console App → Full-Stack Web → AI Chatbot → Kubernetes Deployment → Advanced Cloud Features. Each phase builds incrementally on the previous one, with architectural decisions considering the next phase's requirements. Maintain clean abstractions that support this evolution path.

### IV. Full-Stack Integration
Frontend (Next.js) and Backend (FastAPI) development must be coordinated through shared specifications. Use consistent data models, API contracts, and authentication patterns across both layers. Implement proper separation of concerns while maintaining tight integration between components.

### V. Cloud-Native First
Design all features with cloud deployment in mind, using containerization, microservices patterns, and infrastructure-as-code. Implement stateless services where possible, with externalized configuration and secrets management. Ensure all components are horizontally scalable and resilient.

### VI. MCP-Enabled Tooling
All AI interactions must be enabled through Model Context Protocol (MCP) servers. MCP tools provide standardized interfaces for AI agents to interact with application functionality, enabling natural language processing of user requests into application operations.

### VII. Event-Driven Architecture
Implement event-driven architecture using Kafka (or compatible systems like Redpanda) for decoupled, scalable microservices communication. All task operations (create, update, delete, complete) must publish events to appropriate Kafka topics. Use event schemas for consistent data exchange between services. Implement proper event sourcing and audit trails.

### VIII. Dapr Integration
Integrate Dapr (Distributed Application Runtime) as a sidecar for all services to abstract infrastructure concerns. Use Dapr building blocks including Pub/Sub for Kafka integration, State Management for conversation state, Service Invocation for inter-service communication, Bindings for scheduled operations, and Secrets Management for secure credential handling.

## Advanced Features Requirements

### Recurring Tasks
Implement recurring task functionality using event-driven patterns. When a recurring task is completed, publish an event that triggers the creation of the next occurrence. Support various recurrence patterns (daily, weekly, monthly, etc.) and allow modification of recurring task patterns.

### Due Dates & Reminders
Implement due date functionality with scheduled reminder notifications. Use Dapr's job scheduling capabilities or Kafka-based trigger systems to send reminders at appropriate times. Support different reminder preferences and notification channels.

### Priorities, Tags, Search, Filter, Sort
Implement comprehensive task management features including priority levels, tagging systems, full-text search capabilities, filtering options, and sorting functionality. Ensure these features are properly integrated with the event-driven architecture and maintained consistently across all services.

## Event-Driven Architecture Requirements

### Kafka Topics
- **task-events**: All task CRUD operations published by the Chat API, consumed by Recurring Task Service and Audit Service
- **reminders**: Scheduled reminder triggers published by Chat API when due dates are set, consumed by Notification Service
- **task-updates**: Real-time client synchronization published by Chat API, consumed by WebSocket Service

### Event Schema
All events must follow standardized schemas with required fields:
- Task Event: event_type (string), task_id (integer), task_data (object), user_id (string), timestamp (datetime)
- Reminder Event: task_id (integer), title (string), due_at (datetime), remind_at (datetime), user_id (string)

### Event Processing
Implement proper event processing with error handling, retry mechanisms, and dead letter queues. Ensure event ordering where necessary and implement idempotent event processing to handle duplicate events gracefully.

## Dapr Integration Standards

### Component Configuration
- Use pubsub.kafka for Kafka integration with proper broker configuration
- Use state.postgresql for conversation and task state management
- Use secretstores.kubernetes for secure credential management
- Use pubsub components for inter-service communication

### Service Communication
- Use Dapr service invocation for inter-service communication with built-in retries and circuit breakers
- Implement proper service discovery without hardcoding service URLs
- Use Dapr's mTLS capabilities for secure communication

### State Management
- Store conversation history and state using Dapr's state management
- Implement proper state consistency and conflict resolution
- Use state actors for complex stateful operations

## Technology Stack Requirements

### Core Technologies
- Frontend: Next.js 16+ with TypeScript and Tailwind CSS
- Backend: Python FastAPI with SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- AI Integration: OpenAI Agents SDK with MCP
- Containerization: Docker with Gordon AI assistance
- Orchestration: Kubernetes (Minikube/AKS/GKE/DigitalOcean)
- Package Management: Helm Charts
- AIOps: kubectl-ai and Kagent
- Event Streaming: Kafka or Redpanda Cloud
- Distributed Runtime: Dapr

### Event-Driven Components
- Kafka/Redpanda for event streaming
- Dapr sidecars for infrastructure abstraction
- Strimzi operator for Kafka management (if self-hosted)
- Notification services for reminders
- Recurring task engine services

### Deployment Requirements
- Local development: WSL 2 on Windows, native Linux/Mac
- Frontend hosting: Vercel
- API deployment: Kubernetes clusters (Minikube for local, AKS/GKE/DigitalOcean for cloud)
- Database: Neon Serverless PostgreSQL with proper connection pooling
- Authentication: JWT-based with shared secrets between frontend and backend
- Event Streaming: Managed Kafka (Redpanda Cloud/Confluent) or self-hosted (Strimzi)
- Service Mesh: Dapr with sidecar pattern

## Development Workflow

### Specification Process
1. All features must begin with a complete specification in the /specs directory
2. Specifications must include user stories, acceptance criteria, and technical requirements
3. Specifications must be validated before implementation begins
4. Specifications must map to concrete implementation tasks
5. Event-driven design patterns must be specified for all new features
6. Dapr component configurations must be included in specifications

### Implementation Process
1. Read relevant specification before implementing any feature
2. Reference specifications with @specs/ notation in prompts
3. Implement only what is specified - no feature creep
4. Update specifications if requirements change during development
5. Ensure all task operations publish appropriate events to Kafka
6. Integrate Dapr building blocks as specified in the architecture

### Quality Standards
1. All code must be generated by Claude Code following the specification
2. No manual code changes outside of specification-driven implementation
3. All API endpoints must be properly documented and tested
4. Authentication and authorization must be implemented consistently
5. Error handling must be comprehensive and user-friendly
6. Event processing must be resilient with proper retry and fallback mechanisms
7. Dapr integrations must follow established patterns and standards

### Review and Validation
1. Each phase must be completed before proceeding to the next
2. All deliverables must match the requirements in the Hackathon document
3. Code quality must meet the standards defined in the project documentation
4. Security and performance considerations must be addressed at each phase
5. Event-driven components must be validated for proper decoupling
6. Dapr integrations must be tested for proper abstraction of infrastructure

## Governance

This constitution governs all development activities for the Todo Spec-Driven Development project. All team members and AI agents must comply with these principles. Changes to this constitution require explicit approval and must be documented with a clear rationale. The constitution supersedes all other practices and guidelines not explicitly aligned with these principles. Implementation of new features or architectural changes that conflict with these principles is prohibited without constitutional amendment.

**Version**: 1.1.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2026-02-18
