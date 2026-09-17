from pathlib import Path

from app.data.pipeline import run_pipeline


def test_pipeline_is_reproducible_and_publishes_evidence(tmp_path: Path) -> None:
    first = run_pipeline(tmp_path, seed=42, customer_count=400)
    second = run_pipeline(tmp_path, seed=42, customer_count=400)
    assert first == second
    assert first["customers"] == 400
    assert first["transactions"] == 4800
    assert 0.5 <= first["metrics"]["roc_auc"] <= 1.0
    assert first["model_status"] == "VALIDATED_FOR_PORTFOLIO_DEMO"
    assert (tmp_path / "evidence" / "pipeline_summary.json").exists()
    assert (tmp_path / "artifacts" / "retention_model.joblib").exists()

