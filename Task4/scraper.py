from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime

# Set up WebDriver
driver_path = r"D:\dolat tasks\task4\msedgedriver.exe"
service = Service(driver_path)
driver = webdriver.Edge(service=service)

def scrape_investing_tech_news():
    url = "https://www.investing.com/news/technology-news"
    driver.get(url)
    time.sleep(5)

    headlines = []
    links = []
    dates = []

    articles = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="article-title-link"]')
    for article in articles[:20]:
        headline = article.text.strip()
        link = article.get_attribute("href")
        if headline and link:
            headlines.append(headline)
            links.append(link)

    time_elements = driver.find_elements(By.CSS_SELECTOR, 'time')
    for t in time_elements[:len(headlines)]:
        date_text = t.text.strip()
        dates.append(date_text)

    return pd.DataFrame({
        "Website": ["Investing.com"] * len(headlines),
        "Headline": headlines,
        "Link": links,
        "Date": dates
    })

def scrape_cnbc():
    try:
        url = "https://www.cnbc.com/technology/"
        driver.get(url)
        time.sleep(5)

        headlines = []
        links = []
        dates = []

        articles = driver.find_elements(By.CSS_SELECTOR, 'a.Card-title')
        for article in articles[:20]:
            headline = article.text.strip()
            link = article.get_attribute('href')
            if headline and link:
                headlines.append(headline)
                links.append(link)

        date_elements = driver.find_elements(By.CSS_SELECTOR, 'span.Card-time')
        for d in date_elements[:len(headlines)]:
            dates.append(d.text.strip())

        return pd.DataFrame({
            "Website": ["CNBC"] * len(headlines),
            "Headline": headlines,
            "Link": links,
            "Date": dates
        })

    except Exception as e:
        print(f"❌ CNBC scraping failed: {e}")
        return pd.DataFrame()

def scrape_moneycontrol():
    url = "https://www.moneycontrol.com/news/business/stocks/"
    driver.get(url)
    time.sleep(5)

    headlines = []
    links = []

    articles = driver.find_elements(By.CSS_SELECTOR, 'a[title][href*="/news/"]')

    for article in articles[:20]:
        headline = article.get_attribute("title")
        link = article.get_attribute("href")

        if headline and link and "moneycontrol.com" in link:
            headlines.append(headline.strip())
            links.append(link.strip())

    return pd.DataFrame({
        "Website": ["Moneycontrol"] * len(headlines),
        "Headline": headlines,
        "Link": links,
        "Date": [datetime.now().strftime("%Y-%m-%d")] * len(headlines)
    })

def run_scrapers(selected_sources):
    dfs = []
    if "Investing.com" in selected_sources:
        dfs.append(scrape_investing_tech_news())
    if "CNBC" in selected_sources:
        dfs.append(scrape_cnbc())
    if "Moneycontrol" in selected_sources:
        dfs.append(scrape_moneycontrol())

    if dfs:
        final_df = pd.concat(dfs, ignore_index=True)
        final_df["Scraped At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_df.to_csv("investing_tech_news.csv", index=False)
        print(f"✅ Saved {len(final_df)} articles from {', '.join(selected_sources)} to 'investing_tech_news.csv'")
        return final_df
    else:
        print("❌ No sources selected.")
        return pd.DataFrame()

if __name__ == "__main__":
    run_scrapers(["Investing.com", "CNBC", "Moneycontrol"])
    driver.quit()
