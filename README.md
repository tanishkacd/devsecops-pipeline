# DevSecOps Pipeline: CI/CD with Integrated Container Vulnerability Scanning

A final-year project demonstrating a complete DevSecOps workflow: code push →
Docker build → automated security scan (Trivy) → gated deployment to
Kubernetes. Vulnerable images are blocked before they ever reach a cluster.

## Architecture

```
Developer push (GitHub)
        │
        ▼
  GitHub Actions triggered
        │
        ▼
  ┌─────────────┐
  │ Build Stage │  → builds Docker image
  └─────────────┘
        │
        ▼
  ┌───────────────────┐
  │ Security Scan      │ → Trivy scans image for CVEs
  │ (Trivy)             │   + scans k8s YAML for misconfigs
  └───────────────────┘
        │
   Pass?│Fail → pipeline stops, no deploy
        ▼
  ┌─────────────┐
  │ Push Stage  │  → pushes clean image to Docker Hub
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │ Deploy      │  → kubectl apply to Minikube / EKS
  └─────────────┘
```

## Prerequisites (macOS, Apple Silicon)

Install via Homebrew:

```bash
brew install docker minikube kubectl trivy
```

Also install Docker Desktop for Mac (Apple Silicon build) and start it.

## Local setup

### 1. Clone and enter the project
```bash
cd devsecops-pipeline
```

### 2. Build the image locally and test
```bash
docker build -t devsecops-demo:local .
docker run -p 5000:5000 devsecops-demo:local
curl http://localhost:5000
```

### 3. Scan it manually with Trivy (do this first, before touching GitHub Actions)
```bash
trivy image devsecops-demo:local
```
This is the core deliverable — try it against an older/vulnerable base image
(e.g., change `python:3.11-slim` to `python:3.6` in the Dockerfile) to see
Trivy flag CRITICAL/HIGH CVEs. This "before vs after" comparison is a great
demo for your viva.

### 4. Start Minikube
```bash
minikube start
```

### 5. Deploy manually to Minikube
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service devsecops-demo-service
```

## Setting up the automated pipeline (GitHub Actions)

1. Push this project to a new GitHub repository.
2. Create a Docker Hub account (free) and generate an access token.
3. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
   and add:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
4. Push to `main` — the workflow in `.github/workflows/pipeline.yml` runs
   automatically:
   - Builds the image
   - Scans it with Trivy (fails the pipeline on CRITICAL/HIGH CVEs)
   - Scans your Kubernetes manifests for misconfigurations
   - If clean, pushes the image to Docker Hub
   - Reminds you to deploy (or auto-deploys if you wire up a cloud cluster)

## Demo script for your viva

1. Show a clean run: pipeline passes, image gets pushed.
2. Edit the Dockerfile to use a deliberately old base image
   (e.g., `python:3.6` or `node:10`).
3. Push again — show the pipeline **failing at the security scan stage**,
   listing the CVEs Trivy found, and the push/deploy stages never running.
4. Revert to the safe base image, push again, show it passing and deploying.
5. (Optional) Show the Kubernetes config scan catching a misconfiguration,
   e.g., a container running as root or missing resource limits.

## Extending this project (for extra marks)

- Add a small dashboard (React/HTML page) that reads `trivy-report.json`
  artifacts across runs and shows a vulnerability trend over time.
- Add Slack/email notification on scan failure (GitHub Actions has
  ready-made actions for this).
- Deploy to a real cloud cluster (AWS EKS / GKE / AKS) instead of Minikube,
  and use OIDC or a stored kubeconfig secret in the `deploy` job.
- Add SAST (static code analysis, e.g., Bandit for Python) as an earlier
  stage, before the image is even built.

## Project structure

```
devsecops-pipeline/
├── app/                        # Sample Flask app (the thing being deployed)
│   ├── app.py
│   └── requirements.txt
├── Dockerfile                  # Containerizes the app
├── k8s/
│   ├── deployment.yaml          # K8s Deployment spec
│   └── service.yaml             # K8s Service spec
├── .github/workflows/
│   └── pipeline.yml             # The CI/CD + security scan pipeline
└── README.md
```


