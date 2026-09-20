import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL")

if not BACKEND_URL:
    raise RuntimeError("BACKEND_URL is not configured.")

def ask_question(question: str):
    response = requests.post(
        f"{BACKEND_URL}/query",
        json={"question": question},
        timeout=180,
    )
    response.raise_for_status()
    return response.json()
