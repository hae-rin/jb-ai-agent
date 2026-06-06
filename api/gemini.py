import os
import re
import time
from functools import lru_cache
from google import genai

MODEL = "gemini-2.5-flash"


@lru_cache(maxsize=1)
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate(prompt: str) -> str:
    delays = [5, 15, 30]
    for attempt, delay in enumerate(delays):
        try:
            r = get_client().models.generate_content(model=MODEL, contents=prompt)
            return r.text
        except Exception as e:
            msg = str(e)
            if "503" in msg or "UNAVAILABLE" in msg:
                if attempt < len(delays) - 1:
                    time.sleep(delay)
                    continue
            raise


def generate_with_file(contents: list) -> str:
    r = get_client().models.generate_content(model=MODEL, contents=contents)
    return r.text


def extract(label: str, text: str) -> str:
    escaped = re.escape(label)
    pattern = rf"{escaped}:\s*(.*?)(?=\n[^\d\s][^\n]*:|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""
