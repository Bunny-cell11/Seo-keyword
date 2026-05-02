import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def expand_keywords(seed, max_results=50):
    """
    Use OpenAI to generate keyword candidates from seed.
    """
    if not OPENAI_API_KEY:
        # fallback mock
        return [f"{seed} example {i}" for i in range(1, max_results+1)]
    
    prompt = f"Generate {max_results} SEO keyword suggestions related to '{seed}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1
    )
    text = response.choices[0].text.strip()
    keywords = [k.strip() for k in text.split("\n") if k.strip()]
    return keywords[:max_results]

