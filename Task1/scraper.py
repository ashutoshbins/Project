import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_moneycontrol_links():
    url = "https://www.moneycontrol.com/news/technology/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    print("Moneycontrol status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")
    base = "https://www.moneycontrol.com"
    
    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if text and any(keyword in text.lower() for keyword in ["deal", "investment", "merger", "acquisition", "funding"]):
            full_url = urljoin(base, a['href'])
            links.append({"text": text, "url": full_url})

    return links[:15]  # Return top 15 links

def get_ettech_links():
    url = "https://economictimes.indiatimes.com/tech/startups"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    print("ETTech status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")
    base = "https://economictimes.indiatimes.com"

    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if (
            text 
            and any(keyword in text.lower() for keyword in ["deal", "investment", "funding", "merger", "acquisition"])
            and "/tech/" in href
            and "us" not in href.lower()
        ):
            full_url = urljoin(base, href)
            links.append({"text": text, "url": full_url})

    return links[:15]  # Return top 15 links

def main():
    print("Fetching links from Moneycontrol...")
    moneycontrol_links = get_moneycontrol_links()
    
    print("Fetching links from ETTech...")
    ettech_links = get_ettech_links()
    
    # Combine both lists of links
    all_links = moneycontrol_links + ettech_links
    
    # Print all the links and their associated text
    for item in all_links:
        print(f"Link Text: {item['text']}")
        print(f"Link URL: {item['url']}")
        print()

if __name__ == "__main__":
    main()
