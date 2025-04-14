from newspaper import Article
import requests
def extract_article_content(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to retrieve article. Status code: {response.status_code}"
        
        article = Article(url)
        article.download()
        article.parse()
        
        if len(article.text.split()) > 50:  # Filter out short content
            return article.text
        else:
            return ""  # Skip if content is too short
    except Exception as e:
        return f"Error: {str(e)}"
