from typing import List
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools import Toolkit
import streamlit as st
import requests


# --- CUSTOM TOOLKIT: Exchange Rate Tool Using Twelve Data API ---

class ExchangeRateToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="exchange_rate_tools")
        self.api_key = "381bfbd47d134bea88f30a7d5606ef4f"
        self.supported_pairs = [("USD", "INR"), ("USD", "EUR"), ("EUR", "INR")]
        self.register(self.get_exchange_rates)

    def get_exchange_rates(self) -> str:
        responses = []
        for base, target in self.supported_pairs:
            url = f"https://api.twelvedata.com/exchange_rate?symbol={base}/{target}&apikey={self.api_key}"
            r = requests.get(url)
            data = r.json()
            if 'rate' in data:
                rate = float(data['rate'])
                responses.append(f"**{base}/{target}** = `{rate}`")
            else:
                responses.append(f"Error fetching {base}/{target}: {data.get('message', 'Unknown error')}")
        return "\n".join(responses)


# --- AGENTS SETUP ---

## Web Search Agent for News
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for IT sector news updates",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources", "Summarize news related to the IT sector"],
    show_tool_calls=True,
    markdown=True,
)

## Financial Data Agent (stocks, fundamentals, recommendations)
finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True
        ),
    ],
    instructions=[
        "Format your response using markdown",
        "Use tables to display stock and recommendation data."
    ],
    show_tool_calls=True,
    markdown=True,
)

## Currency Exchange Agent using Toolkit
exchange_agent = Agent(
    name="Exchange Rate Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[ExchangeRateToolkit()],
    instructions=["Provide latest exchange rates for USD, EUR, INR."],
    show_tool_calls=True,
    markdown=True,
)

## Master Agent with Team Collaboration
multi_ai_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_search_agent, finance_agent, exchange_agent],
    instructions=[
        "Display key financial metrics for IT sector companies",
        "Include exchange rates, stock performance, and news summaries",
        "Use tables for clarity and markdown formatting"
    ],
    show_tool_calls=True,
    markdown=True,
)


# --- STREAMLIT DASHBOARD ---

st.set_page_config(page_title="IT Sector Financial Dashboard", layout="wide")

st.title("📊 IT Sector Financial Dashboard")
st.markdown("A centralized dashboard showing stock data, currency rates, and news updates.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
company = st.sidebar.selectbox("Select IT Company", ["AAPL", "MSFT", "GOOGL", "INFY", "TCS.NS", "WIT"])
time_period = st.sidebar.selectbox("Time Range", ["1d", "5d", "1mo", "6mo", "1y"])

# Fetch and Display Financial Data
if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data from AI agents..."):
        # Stock price & analyst data
        stock_query = f"Summarize analyst recommendation and share stock performance for {company}"
        stock_response = finance_agent.run(stock_query).content

        # Currency exchange rates
        exchange_response = exchange_agent.run("Get latest exchange rates for USD, EUR, INR").content

        # Latest IT sector news
        news_response = web_search_agent.run("Give recent news about the IT sector").content

    # Display Results
    st.subheader(f"📈 Stock Performance & Recommendations: {company}")
    st.markdown(stock_response)

    st.subheader("💱 Exchange Rates")
    st.markdown(exchange_response)

    st.subheader("📰 Latest IT Sector News")
    st.markdown(news_response)
