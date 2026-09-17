from __future__ import annotations

import json
from pathlib import Path

import duckdb
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.data.generate import generate_banking_data


NUMERIC_FEATURES = [
    "tenure_months", "digital_adoption", "credit_utilization", "payment_ratio",
    "complaints_90d", "late_payments_6m", "service_calls_90d", "digital_sessions_30d",
    "transaction_count_90d", "spend_90d", "decline_rate_90d",
]
CATEGORICAL_FEATURES = ["region", "segment"]


def _round(value: float) -> float:
    return round(float(value), 4)


def run_pipeline(repo_root: Path, seed: int = 20260917, customer_count: int = 5000) -> dict:
    raw_dir = repo_root / "data" / "raw"
    processed_dir = repo_root / "data" / "processed"
    artifact_dir = repo_root / "artifacts"
    evidence_dir = repo_root / "evidence"
    for directory in (processed_dir, artifact_dir, evidence_dir):
        directory.mkdir(parents=True, exist_ok=True)

    paths = generate_banking_data(raw_dir, seed=seed, customers=customer_count)
    customers = pd.read_csv(paths["customers"])
    transactions = pd.read_csv(paths["transactions"])

    issues = []
    for name, frame, key in (("customers", customers, "customer_id"), ("transactions", transactions, "transaction_id")):
        duplicate_count = int(frame[key].duplicated().sum())
        missing_count = int(frame.isna().sum().sum())
        if duplicate_count:
            issues.append({"dataset": name, "rule": "duplicate_primary_key", "count": duplicate_count})
        if missing_count:
            issues.append({"dataset": name, "rule": "missing_values", "count": missing_count})

    connection = duckdb.connect()
    connection.register("customers", customers)
    connection.register("transactions", transactions)
    features = connection.execute(
        """
        SELECT c.*,
               COUNT(t.transaction_id) AS transaction_count_90d,
               COALESCE(SUM(t.amount), 0) AS spend_90d,
               COALESCE(AVG(t.declined), 0) AS decline_rate_90d
        FROM customers c
        LEFT JOIN transactions t USING (customer_id)
        GROUP BY ALL
        ORDER BY c.customer_id
        """
    ).df()

    x = features[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = features["attrited"]
    x_train, x_test, y_train, y_test, id_train, id_test = train_test_split(
        x, y, features["customer_id"], test_size=0.25, random_state=seed, stratify=y
    )
    preprocessing = ColumnTransformer(
        [
            ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    model = Pipeline([("features", preprocessing), ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    scored_test = features.loc[id_test.index, ["customer_id", "age_group", "segment", "attrited"]].copy()
    scored_test["risk_probability"] = probabilities
    scored_test["predicted_high_risk"] = predictions
    segment_metrics = []
    for group, group_frame in scored_test.groupby("age_group"):
        segment_metrics.append(
            {
                "group": str(group),
                "customers": int(len(group_frame)),
                "actual_attrition_rate": _round(group_frame["attrited"].mean()),
                "high_risk_rate": _round(group_frame["predicted_high_risk"].mean()),
            }
        )
    high_risk_rates = [row["high_risk_rate"] for row in segment_metrics]

    all_probabilities = model.predict_proba(x)[:, 1]
    features["risk_probability"] = all_probabilities
    features["risk_band"] = pd.cut(all_probabilities, bins=[-0.01, 0.35, 0.65, 1.0], labels=["LOW", "MEDIUM", "HIGH"]).astype(str)
    features.to_csv(processed_dir / "customer_features.csv", index=False)
    joblib.dump(model, artifact_dir / "retention_model.joblib")

    metrics = {
        "roc_auc": _round(roc_auc_score(y_test, probabilities)),
        "accuracy": _round(accuracy_score(y_test, predictions)),
        "precision": _round(precision_score(y_test, predictions)),
        "recall": _round(recall_score(y_test, predictions)),
        "brier_score": _round(brier_score_loss(y_test, probabilities)),
    }
    summary = {
        "seed": seed,
        "customers": int(len(customers)),
        "transactions": int(len(transactions)),
        "attrition_rate": _round(y.mean()),
        "review_queue": int((features["risk_band"] != "LOW").sum()),
        "high_risk_customers": int((features["risk_band"] == "HIGH").sum()),
        "data_quality_issues": int(sum(issue["count"] for issue in issues)),
        "data_quality_score": _round(100 * (1 - sum(issue["count"] for issue in issues) / max(1, customers.size + transactions.size))),
        "model_status": "VALIDATED_FOR_PORTFOLIO_DEMO",
        "metrics": metrics,
        "age_group_metrics": segment_metrics,
        "max_high_risk_rate_difference": _round(max(high_risk_rates) - min(high_risk_rates)),
        "limitations": [
            "Synthetic data only",
            "Retention risk is a review signal, not a customer decision",
            "Fairness results are diagnostic and do not establish regulatory compliance",
        ],
    }
    (evidence_dir / "pipeline_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (evidence_dir / "data_quality_issues.json").write_text(json.dumps(issues, indent=2) + "\n")
    return summary

