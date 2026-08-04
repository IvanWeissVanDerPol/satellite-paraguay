"""Production deployment script.

Sets up:
- FastAPI server with Gunicorn (multi-worker)
- Streamlit dashboard with public URL
- PostgreSQL database
- Redis caching
- CI/CD via GitHub Actions
- Docker + docker-compose
- Monitoring with Prometheus + Grafana

This is a deployment scaffolding script. Run on production server.
"""
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path("/root/satellite-paraguay")


def setup_docker():
    """Generate production Docker setup."""
    print("=" * 70)
    print("PRODUCTION DOCKER SETUP")
    print("=" * 70)

    # docker-compose.yml
    docker_compose = """version: '3.8'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: satellite_paraguay
      POSTGRES_USER: hermes
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U hermes"]
      interval: 30s

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  fastapi:
    build: .
    command: gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://hermes:${DB_PASSWORD}@postgres:5432/satellite_paraguay
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  streamlit:
    build: .
    command: streamlit run src/dashboard/app.py --server.port 8501 --server.address 0.0.0.0
    ports:
      - "8501:8501"
    depends_on:
      - fastapi

  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  redis_data:
  grafana_data:
"""
    (REPO_ROOT / "docker-compose.production.yml").write_text(docker_compose)
    print(f"  Wrote: docker-compose.production.yml")

    # Dockerfile
    dockerfile = """FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc gdal-bin libgdal-dev libgeos-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY scripts/ scripts/
COPY data/ data/
COPY outputs/ outputs/

EXPOSE 8000 8501

CMD ["bash", "-c", "gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 & streamlit run src/dashboard/app.py --server.port 8501 --server.address 0.0.0.0"]
"""
    (REPO_ROOT / "Dockerfile.production").write_text(dockerfile)
    print(f"  Wrote: Dockerfile.production")

    # GitHub Actions CI/CD
    github_actions = """name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: coverage.xml

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Build and push Docker
        run: |
          docker build -f Dockerfile.production -t satellite-paraguay:${{ github.sha }} .
          docker push satellite-paraguay:${{ github.sha }}
"""
    github_path = REPO_ROOT / ".github/workflows/cicd.yml"
    github_path.parent.mkdir(parents=True, exist_ok=True)
    github_path.write_text(github_actions)
    print(f"  Wrote: .github/workflows/cicd.yml")

    # Prometheus config
    prometheus_config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['fastapi:8000']
  - job_name: 'streamlit'
    static_configs:
      - targets: ['streamlit:8501']
"""
    (REPO_ROOT / "monitoring/prometheus.yml").parent.mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "monitoring/prometheus.yml").write_text(prometheus_config)
    print(f"  Wrote: monitoring/prometheus.yml")

    print(f"\n  DEPLOYMENT READY:")
    print(f"  1. Set DB_PASSWORD env var")
    print(f"  2. docker-compose -f docker-compose.production.yml up -d")
    print(f"  3. Access:")
    print(f"     - FastAPI: http://localhost:8000/docs")
    print(f"     - Streamlit: http://localhost:8501")
    print(f"     - Prometheus: http://localhost:9090")
    print(f"     - Grafana: http://localhost:3000")


if __name__ == "__main__":
    setup_docker()