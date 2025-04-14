import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def summarize_text(text, max_chunk=1000):
    def query(payload):
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json()[0]['summary_text']
        else:
            raise Exception(f"Hugging Face API Error: {response.status_code} - {response.text}")

    text = ' '.join(text.strip().split())
    summaries = []

    while len(text) > max_chunk:
        split_at = text[:max_chunk].rfind('. ')
        if split_at == -1:
            split_at = max_chunk
        chunk = text[:split_at+1]
        summaries.append(query({"inputs": chunk}))
        text = text[split_at+1:]

    if text:
        summaries.append(query({"inputs": text}))

    return " ".join(summaries)
if __name__ == "__main__":
    input_text = """Hugging Face is creating a tool that democratizes AI, 
    enabling people to access powerful NLP models easily. With their 
    Transformers library and model hub, they allow both researchers and 
    developers to share and use pre-trained models."""
    
    summary = summarize_text(input_text, max_chunk=1000)
    print("📄 Summary:", summary)