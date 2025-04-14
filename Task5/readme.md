# Earnings Call Summarizer

This tool extracts and summarizes earnings call transcripts from PDFs using Hugging Face transformers.

## Features
- Upload PDF or input URL
- Uses `pdfplumber` for accurate extraction
- Summarizes using `facebook/bart-large-cnn`

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
