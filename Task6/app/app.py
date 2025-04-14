import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


# Load model and scaler
model = joblib.load("../model/regression_model.pkl")
scaler = joblib.load("../model/scaler.pkl")

st.title("IT Index Price Forecast")

# Input Ticker
ticker = st.text_input("Enter Index Ticker (default ^NDXT):", value="^NDXT")

# Download Data
data = yf.download(ticker, period="30d", interval="1d")
data.columns = data.columns.get_level_values(0)
if not data.empty:
    st.write("Latest Data", data.tail())

    # Feature Engineering
    data['SMA_5'] = SMAIndicator(data['Close'], window=5).sma_indicator()
    data['SMA_10'] = SMAIndicator(data['Close'], window=10).sma_indicator()
    data['RSI'] = RSIIndicator(data['Close'], window=14).rsi()
    data['Return'] = data['Close'].pct_change()
    data = data.dropna()

    # Use most recent row
    latest = data.iloc[-1]
    features = ['Close', 'Volume', 'SMA_5', 'SMA_10', 'RSI', 'Return']
    X = scaler.transform([latest[features].values])

    prediction = model.predict(X)[0]
    st.subheader(f"Predicted Next-Day Close Price: ${prediction:.2f}")
else:
    st.error("Failed to retrieve data. Check ticker symbol.")

# Actual vs Predicted (last 30 days)
st.subheader("📊 Actual vs Predicted Close Price")

# Prepare input for prediction
features = ['Close', 'Volume', 'SMA_5', 'SMA_10', 'RSI', 'Return']
X_scaled = scaler.transform(data[features])

# Predict for each of the last 30 days
data['Predicted_Close'] = model.predict(X_scaled)

# Plotly interactive chart
fig = go.Figure()

# Actual Close Price
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Close'],
    mode='lines+markers',
    name='Actual Close',
    line=dict(color='blue')
))

# Predicted Close Price
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Predicted_Close'],
    mode='lines+markers',
    name='Predicted Close',
    line=dict(color='orange', dash='dash')
))

# SMA (Trendline)
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['SMA_10'],
    mode='lines',
    name='SMA 10',
    line=dict(color='green', width=2)
))

# Next-day predicted price (dashed horizontal line)
fig.add_trace(go.Scatter(
    x=[data.index[-1], data.index[-1] + pd.Timedelta(days=1)],
    y=[prediction, prediction],
    mode='lines',
    name='Next-Day Prediction',
    line=dict(color='red', dash='dot')
))

# Layout
fig.update_layout(
    title=f"{ticker} - Actual vs Predicted Close Prices (Last 30 Days)",
    xaxis_title='Date',
    yaxis_title='Price',
    legend_title='Legend',
    hovermode='x unified',
    template='plotly_white',
    height=600
)


st.plotly_chart(fig, use_container_width=True)
st.subheader("📉 RSI Trend (Last 30 Days)")

fig_rsi = go.Figure()

# RSI Line
fig_rsi.add_trace(go.Scatter(
    x=data.index,
    y=data['RSI'],
    mode='lines+markers',
    name='RSI',
    line=dict(color='purple')
))

# Overbought (70) line
fig_rsi.add_trace(go.Scatter(
    x=data.index,
    y=[70]*len(data),
    mode='lines',
    name='Overbought (70)',
    line=dict(color='red', dash='dash')
))

# Oversold (30) line
fig_rsi.add_trace(go.Scatter(
    x=data.index,
    y=[30]*len(data),
    mode='lines',
    name='Oversold (30)',
    line=dict(color='green', dash='dash')
))

fig_rsi.update_layout(
    title="Relative Strength Index (RSI) - 14 Day",
    xaxis_title='Date',
    yaxis_title='RSI Value',
    yaxis=dict(range=[0, 100]),
    hovermode='x unified',
    template='plotly_white',
    height=400
)

st.plotly_chart(fig_rsi, use_container_width=True)

