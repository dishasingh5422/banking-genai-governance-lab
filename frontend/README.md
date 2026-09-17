# Dashboard

Install and run:

```bash
npm install
npm run dev
```

The dashboard expects the FastAPI backend at `http://127.0.0.1:8000`. Override it with `VITE_API_URL` when needed.

The interface reads live portfolio, customer, model-card, evaluation and data-quality evidence from the API. It does not use embedded screenshots or hard-coded success claims.
