from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.services import LabService


class CopilotRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    customer_id: str | None = None


service = LabService()
app = FastAPI(title="Banking GenAI Governance Lab", description="Human-reviewed consumer-banking analytics and governed GenAI decision support.", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8088", "http://127.0.0.1:8088"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "banking-genai-governance-api"}


@app.get("/api/portfolio/summary")
def portfolio_summary() -> dict:
    return service.portfolio_summary()


@app.get("/api/customers")
def customers(risk_band: str | None = Query(default=None, pattern="^(LOW|MEDIUM|HIGH)$"), limit: int = Query(default=25, ge=1, le=100)) -> list[dict]:
    return service.list_customers(risk_band=risk_band, limit=limit)


@app.get("/api/customers/{customer_id}")
def customer(customer_id: str) -> dict:
    result = service.customer_detail(customer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result


@app.post("/api/copilot/query")
def copilot(request: CopilotRequest) -> dict:
    return service.copilot(request.question, request.customer_id)


@app.get("/api/governance/model-card")
def model_card() -> dict:
    return service.model_card()


@app.get("/api/evaluations/summary")
def evaluation_summary() -> dict:
    return service.evaluation_summary()


@app.get("/api/data-quality/summary")
def data_quality_summary() -> dict:
    return service.data_quality_summary()
