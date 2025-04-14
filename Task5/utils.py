import pdfplumber
import requests
import tempfile

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def download_pdf_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(response.content)
            tmp.close()
            return tmp.name
    except Exception as e:
        print(f"Download error: {e}")
    return None
