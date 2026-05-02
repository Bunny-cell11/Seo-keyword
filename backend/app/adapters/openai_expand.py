"""
adapters/openai_expand.py

Provide expand_seed(seed, max_candidates, country, language) -> List[str]
- If OPENAI_API_KEY is present and USE_MOCK_OPENAI != "1", attempts a completion call to OpenAI to expand keyword variations.
- Otherwise returns simple deterministic variations (modifiers + question forms + long-tail phrases).
"""

import os
import hashlib
import random
import logging
from typing import List

try:
    import requests
except Exception:
    requests = None

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
USE_MOCK_OPENAI = os.getenv("USE_MOCK_OPENAI", "1")

MODIFIERS = [
    "best", "top", "2025", "near me", "online", "virtual", "for students", "remote",
    "paid", "unpaid", "how to", "benefits", "requirements", "apply", "internship program"
]

def _deterministic_seed(s: str) -> int:
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:8], 16)

def _mock_expand(seed: str, max_candidates: int) -> List[str]:
    rnd = random.Random(_deterministic_seed(seed))
    out = set()
    base = seed.strip()
    # base modifications
    out.add(base)
    for m in MODIFIERS:
        out.add(f"{base} {m}")
        out.add(f"{m} {base}")
    # add some long-tail
    for i in range(20):
        if len(out) >= max_candidates: break
        extra = rnd.choice(["for students", "for beginners", "in 2025", "near me", "online", "abroad"])
        out.add(f"{base} {extra}")
    # ensure deterministic ordering
    out_list = sorted(list(out))[:max_candidates]
    return out_list

async def expand_seed(seed: str, max_candidates: int = 200, country: str = "us", language: str = "en") -> List[str]:
    """
    Returns a list of suggested candidate keywords.
    For demo mode this is synchronous but the function is async to match FastAPI usage.
    """
    if OPENAI_KEY and USE_MOCK_OPENAI.strip() != "1":
        # OPTIONAL: add real OpenAI call using official library or direct HTTP.
        # For simplicity and to avoid dependency, we'll fallback to mock for now.
        logger.info("OPENAI_KEY present but real call is not implemented in this sample. Using mock.")
    return _mock_expand(seed, max_candidates)

