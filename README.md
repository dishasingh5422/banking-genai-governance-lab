# Banking GenAI Governance Lab

A local-first consumer-banking decision-support project that combines predictive analytics with a citation-grounded GenAI assistant. The system is designed for human review: it can summarize evidence and retrieve policy guidance, but it cannot approve credit, change pricing, or make customer-eligibility decisions.

## Problem

Consumer-banking teams work across customer, account, transaction, payment, complaint and digital-interaction data. Analysts need a consistent way to identify retention risk, understand the contributing signals, retrieve relevant servicing guidance and document a reviewable next action.

This project will demonstrate that workflow using reproducible synthetic data and explicit governance controls.

## Planned capabilities

- Reproducible synthetic consumer-banking data with a documented schema
- Python and SQL validation, feature engineering and exploratory analysis
- Interpretable customer-retention baseline with segment-level evaluation
- Citation-grounded retrieval over synthetic policies and model documentation
- GenAI case summaries with safe refusal and human-review boundaries
- Evaluation for retrieval quality, groundedness, prompt injection and PII leakage
- Model card, data lineage, fairness checks, drift monitoring and audit history
- FastAPI backend and responsive React dashboard
- Local deterministic demo mode that does not require paid API credentials
- Automated tests, Docker packaging and continuous integration

## Dashboard

The application will contain six focused workspaces:

1. Executive Overview
2. Customer Risk and Segmentation
3. GenAI Case Copilot
4. Model Governance
5. LLM Evaluation and Monitoring
6. Data Quality

## Repository status

The project is under active development. Features are added in small, reviewable milestones, and the README will distinguish implemented behavior from planned work.

See [docs/product-scope.md](docs/product-scope.md) for the initial product definition and [docs/architecture.md](docs/architecture.md) for the planned system boundaries.

## Safety and limitations

- All customer and banking records are synthetic.
- The application is a portfolio simulation, not a production banking system.
- Generated text is decision support only and requires human review.
- The system must not make credit, pricing, eligibility or adverse-action decisions.
- No real customer information or production credentials belong in this repository.

## License

MIT License. See [LICENSE](LICENSE).

