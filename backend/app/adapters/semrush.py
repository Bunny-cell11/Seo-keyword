"""
adapters/semrush.py

Provides fetch_metrics_bulk(keywords, country) -> list[dict]
Behavior:
- If SEMRUSH_API_KEY env var is set and the HTTP call succeeds, returns real Semrush-like data.
- Otherwise returns deterministic mocked metrics for each keyword (useful for local dev/demo).

Note: This file contains an example HTTP call to Semrush-like endpoints.
Replace endpoint/parameters with your chosen SEO provider's API docs.
"""

import os
import time
import hashlib
import random
import logging
from typing import List, Dict

try:
    import requests
except Exception:
    requests = None

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SEM_KEY = os.getenv("SEMRUSH_API_KEY")
USE_MOCK = os.getenv("USE_MOCK_SEMRUSH", "1")  # default to mocked mode unless set to "0"

# Example mapping to Semrush fields we will return:
# keyword, volume (int), difficulty (float 0-100), cpc (float), num_results (int)

def _deterministic_seed(s: str) -> int:
    # create deterministic seed from keyword
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()
    return int(h[:8], 16)

def _mock_metrics_for(keyword: str) -> Dict:
    rnd = random.Random(_deterministic_seed(keyword))
    volume = int(rnd.uniform(100, 20000))
    difficulty = round(rnd.uniform(5, 85), 2)  # 0 easy -> 100 hard
    cpc = round(rnd.uniform(0.05, 6.00), 2)
    num_results = int(rnd.uniform(50_000, 200_000_000))
    return {
        "keyword": keyword,
        "volume": volume,
        "difficulty": difficulty,
        "cpc": cpc,
        "num_results": num_results,
        "source": "mock"
    }

def _call_semrush_batch(keywords: List[str], country: str = "us") -> List[Dict]:
    """
    Example of how a real semrush call could be structured.
    This code will try to call a Semrush-like endpoint if requests and SEM_KEY exist.
    You must adapt params/URL according to the actual provider (Semrush / DataForSEO / Ahrefs).
    """
    if not requests:
        raise RuntimeError("requests library required for real API calls")

    endpoint = os.getenv("SEMRUSH_ENDPOINT", "https://api.semrush.com/")  # placeholder
    # Semrush has many APIs; adjust for the chosen endpoint and parameters.
    params = {
        "type": "phrase_this",  # placeholder param
        "key": SEM_KEY,
        "export_columns": "Ph,Nq,Dp,Cp,Nr",  # example
        "phrase": ",".join(keywords),
        "database": country.upper()
    }
    logger.info("Attempting real Semrush API call (placeholder endpoint)")

    try:
        resp = requests.get(endpoint, params=params, timeout=20)
        resp.raise_for_status()
        text = resp.text
        # NOTE: Semrush may return CSV; parsing logic required. We'll attempt to parse CSV-like content.
        # For reliability in this sample, if we get anything non-empty we'll fallback to parse a simple format.
        results = []
        # Simplified parsing attempt:
        for kw in keywords:
            # This is illustrative only — replace with actual parsing code.
            results.append({
                "keyword": kw,
                "volume": 1000,
                "difficulty": 50.0,
                "cpc": 0.5,
                "num_results": 100000,
                "source": "semrush_api"
            })
        return results
    except Exception as e:
        logger.warning("Semrush API call failed or is not configured properly: %s", e)
        raise

def fetch_metrics_bulk(keywords: List[str], country: str = "us") -> List[Dict]:
    """
    Fetch volume/difficulty/cpc for a list of keywords.
    Returns a list of dicts with keys: keyword, volume, difficulty, cpc, num_results, source
    """
    # input validation
    if not isinstance(keywords, list):
        raise ValueError("keywords must be a list of strings")
    if len(keywords) == 0:
        return []

    # If configured to use real Semrush and key present, attempt a call
    if SEM_KEY and USE_MOCK.strip() != "1":
        try:
            return _call_semrush_batch(keywords, country)
        except Exception:
            logger.info("Falling back to mock data due to failure in real API call")

    # Otherwise return deterministic mocked data
    results = []
    for kw in keywords:
        metrics = _mock_metrics_for(kw)
        results.append(metrics)
        # be kind to local CPU if many keywords
        time.sleep(0.01)
    return results

if __name__ == "__main__":
    # quick demo
    demo = fetch_metrics_bulk(["global internship", "virtual internship program", "internship abroad"], country="us")
    for r in demo:
        print(r)

