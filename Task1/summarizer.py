import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HUGGINGFACE_TOKEN")

#API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL = "https://api-inference.huggingface.co/models/t5-small"
headers = {"Authorization": f"Bearer {token}"}

def summarize_with_api(text, retries=3):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": 30,
            "max_length": 120,
            "do_sample": False
        }
    }
    

    for i in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            return response.json()[0]['summary_text']
        except Exception as e:
            if i < retries - 1:
                continue
            return f"❌ Summarization failed: {e}"
