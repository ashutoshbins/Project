import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_moneycontrol_links():
    url = "https://www.moneycontrol.com/news/technology/"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    base = "https://www.moneycontrol.com"
    
    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if text and "deal" in text.lower() and len(text.split()) > 4:
            full_url = urljoin(base, a['href'])
            links.append({"text": text, "url": full_url})
    return links[:15]  # top 5

def get_ettech_links():
    url = "https://economictimes.indiatimes.com/tech/startups"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    base = "https://economictimes.indiatimes.com"

    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if (
            text 
            and "deal" in text.lower()
            and len(text.split()) > 4
            and "/tech/" in href
            and "us" not in href.lower()
        ):
            full_url = urljoin(base, href)
            links.append({"text": text, "url": full_url})
    return links[:15]
