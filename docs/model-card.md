# Retention Review Baseline Model Card

## Purpose

The logistic-regression baseline prioritizes synthetic consumer-banking records for analyst review. It is not a customer decision and must not be used for credit approval, pricing, eligibility, adverse action or autonomous treatment.

## Data

The training data contains 5,000 reproducible synthetic customers and 60,000 synthetic transactions. Features describe tenure, digital engagement, credit utilization, payment behavior, complaints, service calls and transaction aggregates. Region and customer segment are included; age is excluded from training and used only for diagnostic evaluation.

## Validation

The committed pipeline evidence records held-out ROC AUC, accuracy, precision, recall and Brier score. A fixed seed supports reproducibility. Segment monitoring reports actual attrition and high-risk selection rates by age group.

## Governance boundaries

- All records are synthetic.
- Scores prioritize review; they do not prescribe action.
- Fairness measurements are diagnostic and do not establish legal or regulatory compliance.
- Material performance or segment changes require investigation before continued use.
- Customer-impacting actions require an authorized human reviewer.

## Known limitations

- Synthetic relationships do not represent a real portfolio.
- The class distribution and feature relationships are intentionally simplified.
- No causal effect is claimed.
- Production drift, operational resilience and institutional model-risk approval are outside this demonstration.

