# Recruiter Walkthrough

## Two-minute demonstration

1. Open **Overview** and explain that every number comes from the reproducible pipeline evidence.
2. Show the 5,000-customer portfolio, 60,000 transactions, review queue and held-out ROC AUC.
3. Explain the age-group monitoring panel as a diagnostic rather than a compliance claim.
4. Open **Customer Review** and select a high-risk synthetic case.
5. Open **Case Copilot**, submit the default retention question and show the customer evidence, human-review boundary and policy citation.
6. Show **Model Governance** for prohibited uses and limitations.
7. Show **Evaluation** for the grounded retrieval, prompt-injection and sensitive-data tests.
8. Finish with **Data Quality** and the deterministic lineage.

## Interview explanation

The project separates predictive analytics, retrieval and generation. The predictive model creates a review signal. Retrieval selects policy evidence. The deterministic copilot composes a bounded case summary and refuses prompt-injection or sensitive-data requests. No component changes account state, and every customer-impacting step requires a human reviewer.

## Honest limitations

The current system uses TF-IDF vector retrieval and deterministic generation so it runs without paid credentials. It demonstrates RAG architecture, evaluation and control design without claiming model fine-tuning, enterprise Spark execution or production-bank deployment.

