# DevSecOps Pipeline: CI/CD with Integrated Container Vulnerability Scanning


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





