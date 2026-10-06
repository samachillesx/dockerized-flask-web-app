# Dockerized Flask Web Application

A containerized Flask web application demonstrating application packaging, environment-based configuration, container networking, Docker Compose orchestration, and application health monitoring.

The project provides a lightweight foundation for understanding how a Python web application moves from local development into a reproducible containerized runtime.

## Overview

This project containerizes a Flask web application using Docker and Docker Compose.

The application exposes a simple web endpoint alongside a dedicated health endpoint that can be consumed by container orchestration and monitoring systems.

Configuration is externalized through environment variables, allowing the same application image to be deployed across different environments without modifying the application source code.

### Key capabilities

* Python Flask web application
* Docker image creation using a dedicated `Dockerfile`
* Reproducible dependency installation
* Environment-based application configuration
* Docker Compose service definition
* Port mapping between host and container
* Application health endpoint
* Container lifecycle management
* Separation of application code from runtime configuration
* Git and Docker build-context hygiene

---

## Architecture

```text
                         Developer Workstation
                                  │
                                  │
                         docker compose
                                  │
                                  ▼
                    ┌────────────────────────┐
                    │     Docker Engine      │
                    │                        │
                    │  ┌──────────────────┐  │
                    │  │   Flask App      │  │
                    │  │                  │  │
                    │  │  :5000           │  │
                    │  │                  │  │
                    │  │  /               │  │
                    │  │  /health         │  │
                    │  └────────┬─────────┘  │
                    │           │            │
                    └───────────┼────────────┘
                                │
                         Port 5000:5000
                                │
                                ▼
                         Host / Browser
```

The application is packaged into a Docker image and executed as a container. Docker Compose provides the declarative runtime configuration.

---

## Technology Stack

| Technology     | Purpose                              |
| -------------- | ------------------------------------ |
| Python         | Application runtime                  |
| Flask          | Web application framework            |
| Docker         | Application containerization         |
| Docker Compose | Container/service orchestration      |
| Git            | Source control                       |
| GitHub         | Repository and project documentation |

---

## Project Structure

```text
dockerized-flask-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
└── README.md
```

### Key files

**`app.py`**
Flask application containing the application routes and environment-based configuration.

**`requirements.txt`**
Defines the Python dependencies required by the application.

**`Dockerfile`**
Defines how the application image is constructed.

**`compose.yaml`**
Defines the containerized application service, networking, port mapping, and runtime environment.

**`.dockerignore`**
Prevents unnecessary files from being included in the Docker build context.

**`.gitignore`**
Prevents local development artifacts, virtual environments, logs, and sensitive configuration from being committed to source control.

---

## Application Endpoints

### Application

```http
GET /
```

Returns the application response together with the configured runtime environment.

Example:

```text
Hello from Docker! Environment: production
```

### Health Check

```http
GET /health
```

Returns a JSON response indicating application health.

```json
{
  "status": "healthy"
}
```

The endpoint provides a lightweight mechanism for container platforms, load balancers, monitoring systems, or orchestration platforms to verify application availability.

---

## Environment Configuration

The application does not hardcode its runtime environment.

Instead, it reads the `APP_ENV` environment variable:

```python
app_env = os.getenv("APP_ENV", "development")
```

The container runtime supplies the configuration:

```yaml
environment:
  APP_ENV: production
```

This separates **application logic** from **environment-specific configuration**.

The same image can therefore be promoted through different environments without modifying the application source.

Example:

```text
Development
APP_ENV=development

Staging
APP_ENV=staging

Production
APP_ENV=production
```

This pattern becomes particularly important when applications are deployed through CI/CD pipelines, Kubernetes, and cloud infrastructure.

---

## Running with Docker

### Build the image

```bash
docker build -t dockerized-flask-app .
```

### Run the container

```bash
docker run -d \
  -p 5000:5000 \
  -e APP_ENV=production \
  --name flask-app \
  dockerized-flask-app
```

Verify the running container:

```bash
docker ps
```

Access the application:

```text
http://localhost:5000
```

Check application health:

```text
http://localhost:5000/health
```

Or from the terminal:

```bash
curl http://localhost:5000/health
```

---

## Running with Docker Compose

Docker Compose provides a declarative way to define and operate the application container.

Start the application:

```bash
docker compose up -d
```

View the running services:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs
```

Follow logs in real time:

```bash
docker compose logs -f
```

Stop and remove the application:

```bash
docker compose down
```

Rebuild after application changes:

```bash
docker compose up -d --build
```

---

## Container Configuration

The Compose configuration exposes the Flask application through port `5000`.

```yaml
services:
  web:
    build: .
    container_name: flask-app
    ports:
      - "5000:5000"
    environment:
      APP_ENV: production
```

The port mapping follows:

```text
HOST:CONTAINER
5000:5000
```

Therefore, requests to:

```text
localhost:5000
```

are forwarded to port `5000` inside the application container.

---

## Health Monitoring

The `/health` endpoint establishes a basic application-level health signal.

This is different from simply verifying that the Docker container is running.

```text
Container running
        │
        ▼
Application responding
        │
        ▼
GET /health
        │
        ▼
HTTP 200
        │
        ▼
Application considered healthy
```

This pattern provides a foundation for implementing Docker health checks and Kubernetes liveness/readiness probes in future deployments.

---

## Docker Build Context

The project uses `.dockerignore` to prevent unnecessary files from being transferred into the Docker build context.

Typical exclusions include:

```text
.git
.gitignore
__pycache__
*.pyc
.env
*.log
```

This reduces build-context size and helps prevent local development artifacts and sensitive configuration from entering the image build process.

---

## Configuration and Secrets

Environment-specific configuration is intentionally kept outside the application source code.

Sensitive values such as:

```text
API keys
Database credentials
Secret keys
Access tokens
```

should not be committed to Git or embedded directly into Docker images.

For production workloads, secrets should be supplied through an appropriate secrets-management mechanism rather than stored in source control.

---

## Operational Workflow

The project follows a simplified container delivery workflow:

```text
Application Source
       │
       ▼
requirements.txt
       │
       ▼
Dockerfile
       │
       ▼
Docker Image
       │
       ▼
Docker Container
       │
       ├── Environment Configuration
       │
       ├── Port Mapping
       │
       └── Health Endpoint
       │
       ▼
Docker Compose
```

This provides a foundation for extending the project into automated CI/CD and orchestration workflows.

---

## Engineering Concepts Demonstrated

This project demonstrates practical understanding of:

* Containerized application packaging
* Docker image construction
* Docker build contexts
* Container lifecycle management
* Port publishing
* Runtime environment variables
* Configuration externalization
* Docker Compose
* Application health endpoints
* Container observability fundamentals
* Reproducible application environments
* Source-control hygiene
* Separation of application and infrastructure concerns

---

## Potential Production Extensions

The current implementation intentionally keeps the application lightweight while establishing patterns that can be extended into a production-oriented deployment.

Potential next steps include:

* Multi-stage Docker builds
* Non-root container execution
* Docker `HEALTHCHECK`
* Gunicorn as the production WSGI server
* Structured application logging
* Nginx reverse proxy
* PostgreSQL or MySQL integration
* Persistent storage
* Docker Compose multi-service architecture
* Automated testing
* Jenkins CI/CD pipeline
* Container image publishing
* Kubernetes deployment
* Kubernetes readiness and liveness probes
* AWS deployment
* Infrastructure provisioning with Terraform

---

## Project Objective

The objective of this project is to demonstrate how a Python web application can be packaged as a reproducible container, configured externally at runtime, exposed through a controlled network interface, and operated using Docker Compose.

It establishes the containerization and operational concepts required for subsequent work with **CI/CD, Kubernetes, AWS, and infrastructure automation**.

---

## Author

**Sam Achilles**

Cloud / DevOps Engineering Portfolio

Focused on building practical experience across:

```text
Linux
Docker
Kubernetes
Terraform
AWS
CI/CD
Infrastructure Automation
```
