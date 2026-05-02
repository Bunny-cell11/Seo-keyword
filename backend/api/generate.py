from adapters.keyword_metrics import get_keyword_volume
from adapters.serpapi import get_keyword_difficulty
from services.keyword_service import score_keyword
from utils.openai_expand import expand_keywords

def generate_keywords_endpoint(request):
    seed_keyword = request.seed
    max_results = request.max_results

    keyword_candidates = expand_keywords(seed_keyword, max_results)

    results = []
    for kw in keyword_candidates:
        volume = get_keyword_volume(kw, geo=request.country)
        difficulty, top_results = get_keyword_difficulty(kw)
        score = score_keyword(volume, difficulty)
        results.append({
            "keyword": kw,
            "volume": volume,
            "difficulty": difficulty,
            "score": score,
            "top_results": top_results
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"seed": seed_keyword, "results": results}

