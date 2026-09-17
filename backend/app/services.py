from __future__ import annotations

import json
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import EVIDENCE_DIR, PROCESSED_DIR, REPO_ROOT


POLICY_DIR = REPO_ROOT / "knowledge" / "policies"


class LabService:
    def __init__(self) -> None:
        summary_path = EVIDENCE_DIR / "pipeline_summary.json"
        self.summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
        features_path = PROCESSED_DIR / "customer_features.csv"
        self.customers = pd.read_csv(features_path) if features_path.exists() else pd.DataFrame()
        self.documents = [{"source": path.stem, "text": path.read_text().strip()} for path in sorted(POLICY_DIR.glob("*.md"))]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.document_matrix = self.vectorizer.fit_transform([doc["text"] for doc in self.documents]) if self.documents else None

    def portfolio_summary(self) -> dict:
        return self.summary

    def list_customers(self, risk_band: str | None, limit: int) -> list[dict]:
        if self.customers.empty:
            return []
        frame = self.customers if not risk_band else self.customers[self.customers["risk_band"] == risk_band]
        columns = ["customer_id", "segment", "region", "risk_band", "risk_probability", "complaints_90d", "late_payments_6m"]
        return frame.sort_values("risk_probability", ascending=False)[columns].head(limit).round(4).to_dict("records")

    def customer_detail(self, customer_id: str) -> dict | None:
        if self.customers.empty:
            return None
        match = self.customers[self.customers["customer_id"] == customer_id]
        if match.empty:
            return None
        return {key: (value.item() if hasattr(value, "item") else value) for key, value in match.iloc[0].to_dict().items()}

    def retrieve(self, question: str, limit: int = 2) -> list[dict]:
        if self.document_matrix is None:
            return []
        scores = cosine_similarity(self.vectorizer.transform([question]), self.document_matrix)[0]
        return [{"source": self.documents[index]["source"], "score": round(float(scores[index]), 4), "excerpt": self.documents[index]["text"][:420]} for index in scores.argsort()[::-1][:limit] if scores[index] > 0]

    def copilot(self, question: str, customer_id: str | None) -> dict:
        lowered = question.lower()
        unsafe = any(term in lowered for term in ("ignore previous", "system prompt", "reveal prompt", "bypass policy"))
        pii = bool(re.search(r"\b(?:\d[ -]*?){12,19}\b|\b\d{3}-\d{2}-\d{4}\b", question))
        if unsafe or pii:
            return {"status": "REFUSED", "reason": "prompt_injection" if unsafe else "sensitive_data", "answer": "I cannot process that request. Use approved, non-sensitive case information.", "citations": []}
        customer = self.customer_detail(customer_id) if customer_id else None
        sources = self.retrieve(question)
        if not sources:
            return {"status": "INSUFFICIENT_EVIDENCE", "answer": "No relevant policy evidence was found. Escalate for human review.", "citations": []}
        context = ""
        if customer:
            context = f"Customer {customer['customer_id']} is in the {customer['risk_band']} review band with score {customer['risk_probability']:.3f}, {int(customer['complaints_90d'])} recent complaints and {int(customer['late_payments_6m'])} late payments. "
        answer = context + "The retrieved guidance supports a documented human review. Confirm the underlying records, discuss approved servicing options, and record the rationale. Do not change credit, pricing or eligibility through this assistant."
        return {"status": "GROUNDED", "answer": answer, "citations": sources, "human_review_required": True}

    def model_card(self) -> dict:
        return {"model": "Logistic Regression Retention Review Baseline", "version": "1.0.0", "status": self.summary.get("model_status", "NOT_TRAINED"), "intended_use": "Prioritize synthetic customer records for analyst review.", "prohibited_uses": ["Credit approval", "Pricing", "Eligibility", "Adverse action", "Autonomous customer treatment"], "metrics": self.summary.get("metrics", {}), "fairness_diagnostic": {"age_group_max_high_risk_rate_difference": self.summary.get("max_high_risk_rate_difference")}, "limitations": self.summary.get("limitations", [])}

    def evaluation_summary(self) -> dict:
        path = EVIDENCE_DIR / "rag_evaluation.json"
        return json.loads(path.read_text()) if path.exists() else {"status": "NOT_RUN", "tests": 0}

    def data_quality_summary(self) -> dict:
        issues = self.summary.get("data_quality_issues", 0)
        return {"score": self.summary.get("data_quality_score", 0), "issues": issues, "status": "PASS" if issues == 0 else "REVIEW"}

