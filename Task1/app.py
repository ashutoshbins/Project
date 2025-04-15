import streamlit as st
from scraper import get_moneycontrol_links, get_ettech_links
from article_extractor import extract_article_content
from summarizer import summarize_text  # Assuming summarize_text is your summarization function

st.set_page_config(page_title="📰 IT & Tech Deal News", layout="wide")

st.title("💼 IT & Tech Deal News Digest (India)")
st.write("Scraping latest headlines and summarizing deals in Indian tech.")

with st.spinner("Fetching news..."):
    all_links = get_moneycontrol_links() + get_ettech_links()

# Loop through all links and display the content
for item in all_links:
    st.subheader(item['text'])
    st.caption(item['url'])
    
    # Extract article content
    content = extract_article_content(item['url'])
    
    # Check if content is long enough (more than 20 words)
    if content and len(content.split()) > 20:
        # Log first 500 characters of content for debugging
        st.write(f"Content for {item['text']} : {content[:500]}")  # Display the first 500 characters of content
        
        # Summarize the article
        summary = summarize_text(content)
        
        # Show summary if successful
        if summary:
            st.success(summary)
        else:
            st.warning(f"Summarization failed for {item['text']}")
    else:
        st.warning(f"Could not extract article or content too short for {item['text']}")
