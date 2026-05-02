# SEO Keyword Agent — Demo & Code

This repository contains a demo-ready Keyword Research AI Agent:
- FastAPI backend (minimal) that expands a seed keyword, enriches with SEO metrics, scores results and returns the top N candidate keywords.
- Adapters for Semrush and SerpApi with **mocked responses by default** so you can run locally without API keys.
- n8n workflow (importable) to orchestrate seed → expansion → enrichment → storage.
- CI workflow (GitHub Actions) example.

---

## What you get in this repo
- `backend/app/` — FastAPI app & adapters
  - `adapters/semrush.py` — Semrush adapter (mocked fallback)
  - `adapters/serpapi.py` — SerpApi adapter (mocked fallback)
  - `adapters/openai_expand.py` — expansion helper (mocked fallback)
  - `scoring.py` — scoring logic
  - `main.py` — example app (see usage below)
- `n8n/n8n_workflow.json` — importable workflow.
- `infra/docker-compose.yml` / `Dockerfile` sample.
- `README.md` — this file.

---

## Quickstart (run locally with mocks)
Requirements:
- Python 3.10+
- pip

1. Clone repo and change directory:
```bash
git clone <your-repo>
cd seo-keyword-agent

