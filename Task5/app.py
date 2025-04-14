import streamlit as st
from utils import extract_text_from_pdf, download_pdf_from_url
from summarizer import summarize_text
import os

st.set_page_config(page_title="Earnings Call Summarizer", layout="wide")
st.title("📈 Earnings Call Summarizer")

if not os.getenv("HF_API_TOKEN"):
    st.warning("⚠️ Hugging Face API token not found. Please set it in .env.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
url_input = st.text_input("Or enter a PDF URL")

if uploaded_file or url_input:
    with st.spinner("Extracting text from PDF..."):
        if uploaded_file:
            text = extract_text_from_pdf(uploaded_file)
        else:
            temp_path = download_pdf_from_url(url_input)
            if temp_path:
                with open(temp_path, "rb") as f:
                    text = extract_text_from_pdf(f)
                os.remove(temp_path)
            else:
                st.error("Failed to download PDF from URL.")
                text = ""

    if text:
        st.subheader("Extracted Text Preview")
        st.text_area("Raw Text", text[:3000], height=200)

        with st.spinner("Generating summary via Hugging Face API..."):
            try:
                summary = summarize_text(text)
                st.subheader("📌 Summary")
                st.success(summary)
            except Exception as e:
                st.error(f"❌ Error: {e}")
