import streamlit as st
import tweepy
import pandas as pd
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# ===================== SETUP =====================

# 🛡 Put your Bearer Token here
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGpt0gEAAAAAGHWaKNLUa1CAmtxVSwwp2QgTGBs%3DmXoyMehwZkOOkIDWuvubftfelQpN1hDnUhazQM9pxLPquhDUg5"

# Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Influencers & keywords
influencers = ["elonmusk","sundarpichai","satyanadella","tim_cook","BillGates","BarackObama","POTUS","jack", "jeffbezos", "neiltyson"]

keywords = ["AI", "tech", "innovation", "deal", "GPT"]

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# ===================== FUNCTIONS =====================

def fetch_tweets(user, keyword, max_results=50):
    query = f'from:{user} "{keyword}" -is:retweet lang:en'
    try:
        tweets = client.search_recent_tweets(query=query,
                                             max_results=max_results,
                                             tweet_fields=["created_at", "text"])
        return tweets.data if tweets and tweets.data else []
    except Exception as e:
        print(f"Error fetching tweets for {user} with keyword '{keyword}':", e)
        return []

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# ===================== STREAMLIT UI =====================

st.title("📊 Social Media Sentiment Analyzer for Tech Influencers")

max_tweets = st.slider("Max tweets per query", min_value=10, max_value=100, value=50)

all_data = []

with st.spinner("Fetching and analyzing tweets..."):
    for user in influencers:
        for keyword in keywords:
            tweets = fetch_tweets(user, keyword, max_results=max_tweets)
            for tweet in tweets:
                sentiment = analyze_sentiment(tweet.text)
                all_data.append({
                    "User": user,
                    "Keyword": keyword,
                    "Date": tweet.created_at.date(),
                    "Tweet": tweet.text,
                    "Sentiment": sentiment
                })

# ===================== DISPLAY RESULTS =====================

df = pd.DataFrame(all_data)

if not df.empty:
    st.success(f"Analyzed {len(df)} tweets ✅")

    # 📊 Pie chart
    st.subheader("Sentiment Breakdown")
    st.write(df["Sentiment"].value_counts())
    fig1, ax1 = plt.subplots()
    df["Sentiment"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, colors=["#4caf50", "#f44336", "#ffc107"])
    ax1.set_ylabel("")
    st.pyplot(fig1)

    # 📅 Time trend
    st.subheader("Sentiment Over Time")
    timeline = df.groupby(['Date', 'Sentiment']).size().unstack().fillna(0)
    st.line_chart(timeline)

    # 📝 Show table
    st.subheader("All Tweets")
    st.dataframe(df[['Date', 'User', 'Keyword', 'Tweet', 'Sentiment']])
else:
    st.warning("No tweets found. Try adjusting keywords or influencers.")