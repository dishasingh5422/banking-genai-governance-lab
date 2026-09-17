# Backend

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
uvicorn app.main:app --reload --port 8000
```

Run tests with `pytest -q`.

The initial summary endpoint intentionally returns zero records and a `NOT_TRAINED` model state. Real metrics will replace these values only after the synthetic data and validation pipeline is implemented.

