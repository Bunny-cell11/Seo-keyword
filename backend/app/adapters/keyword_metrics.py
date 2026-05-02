from pytrends.request import TrendReq

pytrend = TrendReq(hl='en-US', tz=360)

def get_keyword_volume(keyword: str, geo='US'):
    try:
        pytrend.build_payload([keyword], timeframe='today 12-m', geo=geo)
        df = pytrend.interest_over_time()
        if df.empty:
            return 0
        return df[keyword].mean()
    except:
        return 0

