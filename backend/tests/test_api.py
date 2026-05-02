# tests/test_api.py
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
import main

@pytest.mark.asyncio
async def test_generate_endpoint():
    app = main.app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"seed":"global internship","country":"us","language":"en","max_results":5}
        r = await ac.post("/generate", json=payload)
        assert r.status_code == 200
        d = r.json()
        assert "results" in d
        assert len(d["results"]) <= 5

