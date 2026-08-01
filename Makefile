# SatelliteCV-Paraguay — Makefile
# This is the entry point for autonomous execution.

.PHONY: help install bootstrap verify test data-catalog clean dashboard run-paper-% notebook-paper-% autonomous

help:
	@echo "SatelliteCV-Paraguay — Make targets"
	@echo ""
	@echo "Setup:"
	@echo "  make install          — Install all dependencies (pip install -e .)"
	@echo "  make bootstrap        — Full bootstrap: install + data catalog + sample download"
	@echo "  make verify           — Verify all imports + data + tests"
	@echo ""
	@echo "Data:"
	@echo "  make data-catalog     — Generate data catalog from paraguay-geodata/"
	@echo "  make data-local       — Copy local Paraguay data to data/external/"
	@echo "  make data-sentinel    — Download sample Sentinel-2 tiles"
	@echo "  make data-mapbiomas   — Download MapBiomas Paraguay"
	@echo "  make data-all         — Download all data sources"
	@echo ""
	@echo "Papers (run individual paper pipelines):"
	@echo "  make run-paper-1      — Run P0011 Yvytu (deforestation)"
	@echo "  make run-paper-2      — Run P0100 Yvyra (carbon)"
	@echo "  make run-paper-3      — Run P0025 Yrupe (yield)"
	@echo "  make run-paper-4      — Run P0012 Yvy (indigenous)"
	@echo "  make run-paper-5      — Run P0026 Kai (poaching)"
	@echo "  make run-paper-6      — Run P0035 Tatakua (air quality)"
	@echo "  make run-all-papers   — Run all 6 paper pipelines"
	@echo ""
	@echo "Notebooks:"
	@echo "  make notebook-paper-1 — Open notebook for P0011"
	@echo "  make notebook-all     — Open all notebooks"
	@echo ""
	@echo "Validation:"
	@echo "  make validate-paper-1 — Validate P0011 predictions"
	@echo "  make validate-all     — Validate all papers"
	@echo ""
	@echo "Deployment:"
	@echo "  make dashboard        — Run Streamlit dashboard"
	@echo "  make report           — Generate final report"
	@echo ""
	@echo "Autonomous execution:"
	@echo "  make autonomous       — Run full 30-day autonomous plan"

install:
	pip install -e .
	pip install -r requirements.txt

bootstrap: install
	python scripts/bootstrap.py

verify:
	python scripts/verify.py

data-catalog:
	python scripts/data_catalog.py

data-local:
	mkdir -p data/external
	cp -r /root/paraguay-geodata/exports/web/data/* data/external/ || echo "Already copied"

data-sentinel:
	python scripts/download_sentinel_sample.py

data-mapbiomas:
	python scripts/download_mapbiomas.py

data-all: data-local data-sentinel data-mapbiomas

run-paper-1:
	python -m src.papers.p0011_yvytu_deforestation.pipeline

run-paper-2:
	python -m src.papers.p0100_yvyra_carbon_credits.pipeline

run-paper-3:
	python -m src.papers.p0025_yrupe_yield.pipeline

run-paper-4:
	python -m src.papers.p0012_yvy_indigenous.pipeline

run-paper-5:
	python -m src.papers.p0026_kai_poaching.pipeline

run-paper-6:
	python -m src.papers.p0035_tatakua_air_quality.pipeline

run-all-papers: run-paper-1 run-paper-2 run-paper-3 run-paper-4 run-paper-5 run-paper-6

notebook-paper-1:
	jupyter notebook notebooks/p0011_yvytu.ipynb

notebook-all:
	jupyter notebook notebooks/

validate-paper-1:
	python scripts/validate.py --paper 1

validate-all:
	python scripts/validate.py --all

dashboard:
	streamlit run dashboard/app.py

report:
	python scripts/generate_report.py

test:
	pytest tests/ -v

test-fast:
	pytest tests/ -v -m "not slow"

test-coverage:
	pytest tests/ -v --cov=src --cov-report=html

autonomous:
	./run-autonomous.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov/ .mypy_cache
	find . -name "*.pyc" -delete
