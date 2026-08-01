# Multi-stage Dockerfile for SatelliteCV-Paraguay
# Build: docker build -t satellite-paraguay .
# Run: docker run -it --rm -v $(pwd)/data:/app/data satellite-paraguay

# ==========================================
# Stage 1: Base image with Python + system deps
# ==========================================
FROM python:3.10-slim AS base

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    proj-bin \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ==========================================
# Stage 2: Dependencies (cached layer)
# ==========================================
FROM base AS deps

COPY requirements.txt pyproject.toml ./
COPY src/ ./src/

RUN pip install --upgrade pip && \
    pip install -e . && \
    pip install -r requirements.txt

# ==========================================
# Stage 3: Development image (with dev tools)
# ==========================================
FROM deps AS dev

RUN pip install pytest pytest-cov black flake8 isort mypy pre-commit jupyter ipykernel

WORKDIR /app

CMD ["bash"]

# ==========================================
# Stage 4: Production image (minimal)
# ==========================================
FROM deps AS prod

WORKDIR /app

COPY scripts/ ./scripts/
COPY configs/ ./configs/
COPY dashboard/ ./dashboard/
COPY tests/ ./tests/

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '.'); from src.paraguay_admin import load_tile_index; print('OK')" || exit 1

# Default command: run verify
CMD ["python", "scripts/verify.py"]
