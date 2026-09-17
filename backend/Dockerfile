FROM python:3.12-slim

WORKDIR /app/backend
COPY backend ./
RUN python -m pip install --no-cache-dir .
COPY knowledge /app/knowledge
COPY evidence /app/evidence
COPY data /app/data
COPY artifacts /app/artifacts
ENV PYTHONPATH=/app/backend
RUN python scripts/run_pipeline.py && python scripts/evaluate_rag.py

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
