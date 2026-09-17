# Product Scope

## Objective

Build a reproducible portfolio system that shows how predictive analytics and generative AI can support consumer-banking retention and service operations while preserving traceability, human oversight and risk controls.

## Primary user

A banking analytics reviewer who investigates customer-retention risk, reviews contributing signals, consults servicing policies and records a controlled next action.

## Core workflow

1. Load synthetic customer, account, transaction, payment, complaint and digital-interaction data.
2. Validate the data and publish quality findings.
3. Calculate customer features and an interpretable retention-risk score.
4. Review portfolio and segment-level performance.
5. Select a customer case and inspect the evidence.
6. Retrieve relevant policy passages with citations.
7. Generate a grounded case summary and suggested human-review action.
8. Record the reviewer decision and evaluation evidence in an audit trail.

## In scope

- Synthetic data generation
- Data validation and lineage
- SQL analytics and Python feature engineering
- Interpretable predictive baseline
- Segment and fairness evaluation
- Retrieval-augmented generation
- Prompt and retrieval evaluation
- Human-review controls
- API and dashboard
- Local and containerized execution

## Out of scope

- Real customer or bank data
- Autonomous credit, pricing or eligibility decisions
- Production deployment to a financial institution
- Claims of regulatory certification or compliance
- Claims of enterprise-scale Spark infrastructure

## Delivery milestones

1. Repository foundation and interface contract
2. Synthetic data and validation pipeline
3. SQL analytics and predictive baseline
4. FastAPI service and dashboard shell
5. Case review and retrieval workflow
6. GenAI evaluation and governance evidence
7. Packaging, CI and recruiter walkthrough

## Acceptance criteria

- A new reviewer can run the project using documented commands.
- Generated data is deterministic for a fixed seed.
- Every dashboard metric traces to a data or model artifact.
- Every GenAI response includes retrieved evidence or refuses safely.
- Tests cover pipeline, API, retrieval and governance behavior.
- Measured results are stored as machine-readable evidence.
- Limitations and non-production boundaries remain visible.

