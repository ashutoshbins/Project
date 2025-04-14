import streamlit as st
import pandas as pd
from scraper import run_scrapers  # Assuming your scraper is saved as scraper.py

st.set_page_config(page_title="Tech News Scraper", layout="wide")

st.title("📰 Tech News Scraper")
st.markdown("Choose your news sources and click **Scrape News** to fetch the latest tech headlines.")

# News source options
sources = ["Investing.com", "CNBC"]
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
                file_name="investing_tech_news.csv",
                mime="text/csv"
            )
        else:
            st.warning("No articles were scraped.")
    else:
        st.warning("Please select at least one source.")

