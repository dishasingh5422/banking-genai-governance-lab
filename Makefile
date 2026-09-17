.PHONY: setup pipeline test build run

setup:
	python3 -m venv backend/.venv
	backend/.venv/bin/python -m pip install -e 'backend[dev]'
	cd frontend && npm ci

pipeline:
	cd backend && .venv/bin/python scripts/run_pipeline.py && .venv/bin/python scripts/evaluate_rag.py

test:
	cd backend && .venv/bin/python -m pytest -q
	cd frontend && npm run lint

build:
	cd frontend && npm run build

run:
	docker compose up --build

