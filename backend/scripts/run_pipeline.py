from pathlib import Path

from app.data.pipeline import run_pipeline


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    result = run_pipeline(root)
    print(f"Generated {result['customers']} customers and {result['transactions']} transactions")
    print(f"ROC AUC: {result['metrics']['roc_auc']}")

