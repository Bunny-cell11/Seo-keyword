from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from adapters.openai_expand import expand_seed
from adapters.semrush import fetch_metrics_bulk
from adapters.serpapi import serp_snapshot
from scoring import score_keywords

app = FastAPI()

class GenerateRequest(BaseModel):
    seed: str
    country: str = "us"
    language: str = "en"
    max_results: int = 50

@app.post("/generate")
async def generate(req: GenerateRequest):
    # 1) Expand seed into candidates (OpenAI + autocomplete heuristics)
    candidates = await expand_seed(req.seed, req.max_results*3, req.country, req.language)

    # 2) Enrich with metrics via Semrush (volume, difficulty, cpc)
    enriched = fetch_metrics_bulk(candidates, req.country)

    # 3) Score and filter down to top N
    ranked = score_keywords(enriched, top_n=req.max_results)

    # 4) Optionally run SERP snapshot for top candidates
    for k in ranked[:5]:
        k["serp_snapshot"] = serp_snapshot(k["keyword"], req.country)

    return {"seed": req.seed, "results": ranked}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

