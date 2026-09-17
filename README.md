# Banking GenAI Governance Lab

[![Project validation](https://github.com/dishasingh5422/banking-genai-governance-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/dishasingh5422/banking-genai-governance-lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A full-stack, local-first consumer-banking decision-support project combining predictive analytics with citation-grounded GenAI controls. It uses reproducible synthetic data and keeps every customer-impacting action under human review.

> Portfolio simulation only. This is not an official bank system, regulatory compliance product or production decision engine.

## Verified evidence

The current committed pipeline produces:

- 5,000 synthetic customers and 60,000 synthetic transactions
- DuckDB SQL transaction aggregation and Python feature engineering
- Logistic-regression retention review baseline with held-out ROC AUC of 0.766
- 2,694 medium/high-priority review cases and 829 high-risk cases
- Age-group selection-rate diagnostics with a maximum observed difference of 4.7 percentage points
- Citation-grounded policy retrieval and customer-aware case summaries
- Prompt-injection and sensitive-data refusal controls
- 5 of 5 passing retrieval and safety evaluation scenarios
- 5 passing backend tests
- Responsive React dashboard and validated production build

The reproducible metrics are stored in [evidence/pipeline_summary.json](evidence/pipeline_summary.json) and [evidence/rag_evaluation.json](evidence/rag_evaluation.json).

## Product workflow

1. Generate deterministic customer and transaction data.
2. Validate primary keys and missing values.
3. Aggregate transaction behavior with DuckDB SQL.
4. Train and validate an interpretable retention-risk baseline.
5. Prioritize synthetic customer records for human review.
6. Retrieve relevant policy passages using TF-IDF vector search.
7. Generate a bounded case summary with citations and prohibited-use controls.
8. Review model performance, segment diagnostics, RAG tests and data lineage in the dashboard.

## Dashboard

The responsive interface includes:

- **Executive Overview** — portfolio, queue and validation metrics
- **Customer Review** — prioritized synthetic cases and risk signals
- **Case Copilot** — grounded summaries with policy citations
- **Model Governance** — intended use, limitations and prohibited actions
- **Evaluation** — retrieval, injection and sensitive-data test evidence
- **Data Quality** — validation status and lineage

## Architecture

```text
Synthetic generator -> validation -> DuckDB SQL -> feature pipeline
                                               -> logistic baseline -> API -> dashboard
Policy documents -> TF-IDF vector retrieval -> governed copilot ----^
Evaluation cases --------------------------------> evidence JSON ----^
```

The predictive model creates a review signal. Retrieval selects policy evidence. The copilot composes a bounded summary and cannot change account state.

## Technology

- **Data and ML:** Python, pandas, NumPy, DuckDB, SQL, scikit-learn, joblib
- **API:** FastAPI, Pydantic, Uvicorn
- **GenAI controls:** TF-IDF vector retrieval, cited evidence, deterministic generation, refusal tests
- **Frontend:** React, TypeScript, Vite, responsive CSS
- **Quality:** pytest, TypeScript checks, GitHub Actions
- **Packaging:** Docker and Docker Compose

PySpark, model fine-tuning and production-bank deployment are not claimed. See [docs/model-card.md](docs/model-card.md) for limitations.

## Run locally

### Prerequisites

- Python 3.11 or later
- Node.js 22 or later

### Setup and validation

```bash
make setup
make pipeline
make test
make build
```

Start the API:

```bash
cd backend
.venv/bin/uvicorn app.main:app --reload --port 8000
```

In another terminal, start the dashboard:

```bash
cd frontend
npm run dev
```

Open `http://127.0.0.1:5173`.

### Docker

```bash
docker compose up --build
```

Open the dashboard at `http://localhost:8088` and the API documentation at `http://localhost:8010/docs`.

## Test and evidence commands

```bash
cd backend
.venv/bin/python scripts/run_pipeline.py
.venv/bin/python scripts/evaluate_rag.py
.venv/bin/python -m pytest -q

cd ../frontend
npm run lint
npm run build
```

## Documentation

- [Product scope](docs/product-scope.md)
- [Architecture](docs/architecture.md)
- [Model card](docs/model-card.md)
- [Recruiter walkthrough](docs/recruiter-walkthrough.md)

## Safety boundaries

- All data is synthetic.
- Generated text is decision support only.
- Credit, pricing, eligibility and adverse-action decisions are prohibited.
- Sensitive-data and prompt-injection requests are refused.
- Fairness metrics are diagnostic and do not establish regulatory compliance.
- No real customer information or production credentials belong in this repository.

## License

MIT License. See [LICENSE](LICENSE).
