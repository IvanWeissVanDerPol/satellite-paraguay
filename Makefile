# SatelliteCV-Paraguay — Makefile
# Entry point for all common tasks.

.PHONY: help install bootstrap verify test test-fast test-coverage test-property test-performance test-integration lint format notebook-paper-% run-paper-% dashboard api observability report autonomous clean docker-build docs pre-commit-install pre-commit-run audit-deps mutation reproduce cron-install

help:
	@echo "SatelliteCV-Paraguay — Make targets"
	@echo ""
	@echo "Setup:"
	@echo "  make install               — Install all dependencies (pip install -e .)"
	@echo "  make bootstrap             — Full bootstrap: install + data catalog + sample download"
	@echo "  make verify                — Verify all imports + data + tests"
	@echo "  make pre-commit-install    — Install pre-commit hooks"
	@echo "  make pre-commit-run        — Run pre-commit on all files"
	@echo ""
	@echo "Data:"
	@echo "  make data-catalog          — Generate data catalog from paraguay-geodata/"
	@echo "  make data-local            — Copy local Paraguay data to data/external/"
	@echo "  make data-sentinel         — Download sample Sentinel-2 tiles"
	@echo "  make data-mapbiomas        — Download MapBiomas Paraguay"
	@echo "  make data-all              — Download all data sources"
	@echo ""
	@echo "Code quality:"
	@echo "  make lint                  — Run black + flake8 + isort + mypy"
	@echo "  make format                — Auto-format with black + isort"
	@echo "  make test                  — Run pytest"
	@echo "  make test-fast             — Skip slow tests"
	@echo "  make test-coverage         — With coverage report"
	@echo ""
	@echo "Papers (run individual paper pipelines):"
	@echo "  make run-paper-1           — P0011 Yvytu (deforestation)"
	@echo "  make run-paper-2           — P0100 Yvyra (carbon)"
	@echo "  make run-paper-3           — P0025 Yrupe (yield)"
	@echo "  make run-paper-4           — P0012 Yvy (indigenous)"
	@echo "  make run-paper-5           — P0026 Kai (poaching)"
	@echo "  make run-paper-6           — P0035 Tatakua (air quality)"
	@echo "  make run-all-papers        — Run all 6 paper pipelines"
	@echo ""
	@echo "Baselines:"
	@echo "  make baselines-1           — P0011 baselines (Random Forest, U-Net, etc.)"
	@echo "  make baselines-2           — P0100 baselines (Linear, RF, persistence)"
	@echo "  make baselines-3           — P0035 baselines (mean, persistence, trend)"
	@echo ""
	@echo "Notebooks:"
	@echo "  make notebook-paper-1     — Open P0011 notebook"
	@echo "  make notebook-all          — Open all notebooks"
	@echo "  make notebook-eda          — Open EDA notebooks"
	@echo ""
	@echo "Validation:"
	@echo "  make validate-paper-1      — Validate P0011 predictions"
	@echo "  make validate-all          — Validate all papers"
	@echo ""
	@echo "Deployment:"
	@echo "  make dashboard             — Run Streamlit dashboard"
	@echo "  make api                   — Run FastAPI server"
	@echo "  make report                — Generate final report"
	@echo ""
	@echo "Thesis:"
	@echo "  make thesis-pdf            — Compile thesis to PDF (requires pdflatex)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build          — Build Docker image"
	@echo "  make docker-run            — Run in Docker container"
	@echo "  make docker-compose-up     — Start docker-compose stack"
	@echo ""
	@echo "Autonomous execution:"
	@echo "  make autonomous            — Run full 30-day autonomous plan"
	@echo ""
	@echo "Testing & automation:"
	@echo "  make test-property         — Property-based tests (hypothesis)"
	@echo "  make test-performance      — Performance benchmarks"
	@echo "  make test-integration      — Integration tests"
	@echo "  make audit-deps            — Dependency audit"
	@echo "  make mutation              — Mutation testing (slow)"
	@echo "  make reproduce             — Reproducibility verification"
	@echo "  make cron-install          — Install crontab"
	@echo "  make observability         — Run observability dashboard"

install:
	pip install -e ".[dev]"
	pip install -r requirements.txt

pre-commit-install:
	pre-commit install
	@echo "Pre-commit hooks installed"

pre-commit-run:
	pre-commit run --all-files

bootstrap: install
	python3 scripts/bootstrap.py

verify:
	python3 scripts/verify.py

lint:
	black --check --diff src/ tests/ scripts/
	isort --check-only --diff src/ tests/ scripts/
	flake8 src/ tests/ scripts/ --max-line-length=120 --extend-ignore=E203,W503,F401,F841

format:
	black src/ tests/ scripts/ --line-length=120
	isort src/ tests/ scripts/ --profile=black --line-length=120

data-catalog:
	python3 scripts/data_catalog.py

data-local:
	mkdir -p data/external
	cp -r /root/paraguay-geodata/exports/web/data/* data/external/ || echo "Already copied"

data-sentinel:
	python3 scripts/download_sentinel_sample.py

data-mapbiomas:
	python3 scripts/download_mapbiomas.py

data-all: data-local data-sentinel data-mapbiomas

run-paper-1:
	python3 -m src.papers.p0011_yvytu_deforestation.pipeline

run-paper-2:
	python3 -m src.papers.p0100_yvyra_carbon_credits.pipeline

run-paper-3:
	python3 -m src.papers.p0025_yrupe_yield.pipeline

run-paper-4:
	python3 -m src.papers.p0012_yvy_indigenous.pipeline

run-paper-5:
	python3 -m src.papers.p0026_kai_poaching.pipeline

run-paper-6:
	python3 -m src.papers.p0035_tatakua_air_quality.pipeline

run-all-papers: run-paper-1 run-paper-2 run-paper-3 run-paper-4 run-paper-5 run-paper-6

baselines-1:
	python3 -m src.baselines.p0011_yvytu_baselines

baselines-2:
	python3 -m src.baselines.p0100_yvyra_baselines

baselines-3:
	python3 -m src.baselines.p0035_tatakua_baselines

notebook-paper-1:
	jupyter notebook notebooks/p0011_yvytu.ipynb

notebook-all:
	jupyter notebook notebooks/

notebook-eda:
	jupyter notebook notebooks/eda_paraguay_geodata.ipynb

validate-paper-1:
	python3 scripts/validate.py --paper 1

validate-all:
	python3 scripts/validate.py --all

dashboard:
	streamlit run dashboard/app.py

api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

report:
	python3 scripts/generate_report.py

thesis-pdf:
	cd thesis && pdflatex main.tex && pdflatex main.tex && bibtex main && pdflatex main.tex
	@echo "Thesis PDF: thesis/main.pdf"

test:
	pytest tests/ -v

test-fast:
	pytest tests/ -v -m "not slow and not gpu and not performance and not network"

test-coverage:
	pytest tests/ -v --cov=src --cov=scripts --cov-report=html --cov-report=xml --cov-fail-under=30

test-property:
	pytest tests/test_properties.py -m property -v --no-cov --hypothesis-seed=42

test-performance:
	pytest tests/test_performance.py -m performance --no-cov --benchmark-only --benchmark-autosave

test-integration:
	pytest tests/test_integration.py -m integration --no-cov -v

audit-deps:
	python3 scripts/audit_dependencies.py

mutation:
	python3 scripts/mutation_testing.py

reproduce:
	python3 scripts/verify_reproducibility.py

cron-install:
	@echo "Installing crontab..."
	@crontab scripts/crontab.txt || echo "Failed to install. Run: crontab scripts/crontab.txt"

observability:
	streamlit run src/observability_dashboard.py

docker-build:
	docker build -t satellite-paraguay:latest .

docker-run:
	docker run -it --rm -v $(PWD)/data:/app/data -v /root/paraguay-geodata:/paraguay-geodata:ro satellite-paraguay:latest

docker-compose-up:
	docker-compose up -d

autonomous:
	./run-autonomous.sh

docs:
	@echo "Docs are in docs/"
	ls docs/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov/ .mypy_cache
	find . -name "*.pyc" -delete
