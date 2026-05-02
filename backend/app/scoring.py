# naive scoring: normalize volume and difficulty
def normalize(series):
    mn = min(series); mx = max(series)
    if mx == mn: return [0.5]*len(series)
    return [(v-mn)/(mx-mn) for v in series]

def score_keywords(rows, top_n=50, difficulty_weight=0.9):
    vols = [r['volume'] or 0 for r in rows]
    diffs = [r['difficulty'] or 100 for r in rows]  # higher means harder
    nvol = normalize(vols)
    ndiff = normalize(diffs)
    for i,r in enumerate(rows):
        r['score'] = nvol[i] - difficulty_weight * ndiff[i]
    rows.sort(key=lambda x: x['score'], reverse=True)
    return rows[:top_n]

