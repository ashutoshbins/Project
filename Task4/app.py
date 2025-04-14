import streamlit as st
import pandas as pd
from scraper import run_scrapers  # Make sure scraper.py includes Moneycontrol function

st.set_page_config(page_title="Tech & Market News Scraper", layout="wide")

st.title("📰 Tech & Market News Scraper")
st.markdown("Choose your news sources and click **Scrape News** to fetch the latest headlines from trusted platforms.")

# Updated source list
sources = ["Investing.com", "CNBC", "Moneycontrol"]
selected_sources = st.multiselect("Select news sources:", sources, default=sources)

if st.button("🔍 Scrape News"):
    if selected_sources:
        with st.spinner("Scraping in progress..."):
            df = run_scrapers(selected_sources)

        if not df.empty:
            st.success(f"✅ Fetched {len(df)} articles.")
            st.dataframe(df, use_container_width=True)

            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="news_headlines.csv",
                mime="text/csv"
            )
        else:
            st.warning("No articles were scraped.")
    else:
        st.warning("Please select at least one source.")
