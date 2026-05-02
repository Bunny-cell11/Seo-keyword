# tests/test_scoring.py
import pytest
from scoring import score_keywords

def make_rows(n=5):
    rows = []
    for i in range(n):
        rows.append({
            "keyword": f"k{i}",
            "volume": (i+1)*100,
            "difficulty": (n-i)*10  # varied
        })
    return rows

def test_score_output_length():
    rows = make_rows(10)
    top = score_keywords(rows, top_n=5)
    assert len(top) == 5

def test_score_ordering():
    rows = make_rows(6)
    top = score_keywords(rows, top_n=6)
    # highest volume and low difficulty should have highest score
    assert top[0]["volume"] >= top[-1]["volume"]

