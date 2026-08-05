"""Production deployment template generation.

Generates docker-compose, Dockerfile, GitHub Actions, and Prometheus configs.
"""


def build_docker_compose() -> str:
    """Generate production docker-compose.yml content."""
    return """version: '3.8'

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
      DATABASE_URL: postgresql://hermes:***@postgres:5432/satellite_paraguay
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


def build_dockerfile() -> str:
    """Generate production Dockerfile content."""
    return """FROM python:3.12-slim

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


def build_github_actions() -> str:
    """Generate GitHub Actions CI/CD workflow content."""
    return """name: CI/CD

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


def build_prometheus_config() -> str:
    """Generate Prometheus configuration content."""
    return """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['fastapi:8000']
  - job_name: 'streamlit'
    static_configs:
      - targets: ['streamlit:8501']
"""


def write_docker_compose(content: str, output_path) -> None:
    """Write docker-compose.production.yml."""
    output_path.write_text(content)


def write_dockerfile(content: str, output_path) -> None:
    """Write Dockerfile.production."""
    output_path.write_text(content)


def write_github_actions(content: str, output_path) -> None:
    """Write .github/workflows/cicd.yml (creates parent dirs)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)


def write_prometheus_config(content: str, output_path) -> None:
    """Write monitoring/prometheus.yml (creates parent dirs)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)