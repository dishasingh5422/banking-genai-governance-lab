from datetime import UTC, datetime

from fastapi import FastAPI
from pydantic import BaseModel


class PortfolioSummary(BaseModel):
    customers: int
    review_queue: int
    high_risk_customers: int
    data_quality_score: float
    model_status: str
    generated_at: datetime


app = FastAPI(
    title="Banking GenAI Governance Lab",
    description="Human-reviewed consumer-banking analytics and GenAI decision support.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "banking-genai-governance-api"}


@app.get("/api/portfolio/summary", response_model=PortfolioSummary)
def portfolio_summary() -> PortfolioSummary:
    """Return deterministic placeholder metrics until the data pipeline lands."""
    return PortfolioSummary(
        customers=0,
        review_queue=0,
        high_risk_customers=0,
        data_quality_score=100.0,
        model_status="NOT_TRAINED",
        generated_at=datetime.now(UTC),
    )

