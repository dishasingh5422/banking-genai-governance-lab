from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_reports_service_identity() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "banking-genai-governance-api",
    }


def test_portfolio_summary_is_explicitly_untrained() -> None:
    response = client.get("/api/portfolio/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["customers"] == 0
    assert payload["model_status"] == "NOT_TRAINED"
    assert payload["data_quality_score"] == 100.0

