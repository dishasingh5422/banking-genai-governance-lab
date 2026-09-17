# Planned Architecture

## Components

### Data layer

- Synthetic data generator
- Raw and processed Parquet or CSV datasets
- DuckDB for local analytical SQL
- Optional local PySpark transformation path

### Analytics layer

- Data-quality rules
- Feature engineering
- Logistic-regression baseline
- Segment, fairness and drift evaluation
- Versioned model card and metrics

### GenAI layer

- Policy-document ingestion
- Local embeddings and vector retrieval
- Provider-independent generation interface
- Deterministic no-key demo response path
- Evaluation for citation quality, groundedness, refusal and safety

### Application layer

- FastAPI service
- React and TypeScript dashboard
- Reviewer decisions and audit events

## System boundaries

The predictive model produces a review signal rather than a customer decision. The retrieval layer returns source passages. The generation layer may summarize those inputs, but it cannot change account state. The reviewer remains responsible for the recorded action.

## Initial API contract

- `GET /health`
- `GET /api/portfolio/summary`
- `GET /api/customers`
- `GET /api/customers/{customer_id}`
- `POST /api/copilot/query`
- `GET /api/governance/model-card`
- `GET /api/evaluations/summary`
- `GET /api/data-quality/summary`

Endpoints will be implemented and tested incrementally. This document describes the target contract, not current completion.

