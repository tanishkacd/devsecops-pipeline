# Use a slim, specific base image (avoid 'latest' tag for reproducibility)
FROM python:3.11-slim

# Create a non-root user (good practice, also helps you avoid some Trivy/K8s findings)
RUN useradd -m appuser

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
