# tests/test_adapters_mock.py
import pytest
from adapters import semrush, serpapi, openai_expand

def test_semrush_mock():
    kws = ["global internship", "internship abroad"]
    res = semrush.fetch_metrics_bulk(kws, country="us")
    assert isinstance(res, list)
    assert res[0]["keyword"] == kws[0]
    assert "volume" in res[0]

def test_serpapi_mock():
    snap = serpapi.serp_snapshot("global internship", country="us")
    assert snap["keyword"] == "global internship"
    assert isinstance(snap["top_results"], list)
    assert len(snap["top_results"]) >= 1

@pytest.mark.asyncio
async def test_openai_expand_mock():
    out = await openai_expand.expand_seed("global internship", max_candidates=20)
    assert isinstance(out, list)
    assert len(out) <= 20

