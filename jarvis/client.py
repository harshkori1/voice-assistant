import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
# ✅ Use a working model
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}


def ask_ai(prompt):
    try:
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()

        # Handle both model types (list or dict)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "No text generated.")
        elif isinstance(data, dict) and "error" in data:
            return f"API Error: {data['error']}"
        else:
            return str(data)

    except Exception as e:
        return f"Error: {e}"
