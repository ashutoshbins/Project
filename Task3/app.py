import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import requests

# Define the toolkit for fetching stock prices using yfinance
class StockPriceToolkit:
    def __init__(self):
        # Adding the '.NS' suffix for NSE-listed companies
        self.companies = ["INFY.NS", "TCS.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"]

    def get_stock_prices(self) -> str:
        responses = []
        for company in self.companies:
            try:
                stock = yf.Ticker(company)
                data = stock.history(period="1d")  # Get stock data for the current day

                # Flatten multi-level columns (yfinance returns columns as multi-level tuple)
                data.columns = data.columns.get_level_values(0)

                if not data.empty:
                    # Get the 'Close' price for the most recent day
                    price = data['Close'].iloc[-1]
                    responses.append(f"{company} stock price = `{price}`")
                else:
                    responses.append(f"Error: No data for {company}.")
            except Exception as e:
                responses.append(f"Error fetching {company} stock price: {e}")
        
        return "\n".join(responses)

# Define the toolkit for fetching exchange rates
class ExchangeRateToolkit:
    def __init__(self):
        self.api_key = "381bfbd47d134bea88f30a7d5606ef4f"
        self.supported_pairs = [("USD", "INR"), ("EUR", "INR"), ("JPY", "INR"), ("CHF", "INR")]

    def get_exchange_rates(self) -> str:
        responses = []
        for base, target in self.supported_pairs:
            url = f"https://api.twelvedata.com/exchange_rate?symbol={base}/{target}&apikey={self.api_key}"
            try:
                r = requests.get(url)
                data = r.json()
                if 'rate' in data:
                    rate = float(data['rate'])
                    responses.append(f"**{base}/{target}** = `{rate}`")
                else:
                    responses.append(f"Error fetching {base}/{target}: {data.get('message', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                responses.append(f"Error fetching {base}/{target}: {str(e)}")
        return "\n".join(responses)

# Utility function to calculate percentage change
def calculate_percentage_change(df: pd.DataFrame) -> pd.DataFrame:
    df['Percentage Change'] = df['Close'].pct_change() * 100
    return df

# Utility function to plot the data
def plot_data(df_exchange: pd.DataFrame, df_stock: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Exchange Rates
    ax.plot(df_exchange['Date'], df_exchange['Percentage Change'], label='Exchange Rate Change', color='blue', marker='o')
    
    # Plot Stock Prices
    ax.plot(df_stock['Date'], df_stock['Percentage Change'], label='Stock Price Change', color='green', marker='x')
    
    ax.set_title('Exchange Rate and Stock Price Changes')
    ax.set_xlabel('Date')
    ax.set_ylabel('Percentage Change (%)')
    ax.legend(loc='best')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Function to send alerts (for demonstration, this will just print an alert message)
def send_alert(message: str):
    print(f"ALERT: {message}")  # In real implementation, this could send an email or SMS

# Initialize toolkits
exchange_toolkit = ExchangeRateToolkit()
stock_toolkit = StockPriceToolkit()

# Fetch data from the toolkits
exchange_rates = exchange_toolkit.get_exchange_rates()
stock_prices = stock_toolkit.get_stock_prices()

# Display fetched data in the Streamlit app
st.title("Currency Impact Analyzer for IT Companies")

st.write("### Exchange Rates")
st.text(exchange_rates)

st.write("### Stock Prices")
st.text(stock_prices)

# Mock data (replace this with actual API data)
df_exchange = pd.DataFrame({
    'Date': pd.date_range(start="2025-04-01", periods=5, freq='D'),
    'Close': [82.3, 83.1, 81.8, 82.5, 83.2]
})

df_stock = pd.DataFrame({
    'Date': pd.date_range(start="2025-04-01", periods=5, freq='D'),
    'Close': [1200, 1210, 1195, 1205, 1215]
})

# Calculate percentage change
df_exchange = calculate_percentage_change(df_exchange)
df_stock = calculate_percentage_change(df_stock)

# Display DataFrames as tables
st.write("### Exchange Rate Data (Percentage Change)")
st.dataframe(df_exchange)

st.write("### Stock Price Data (Percentage Change)")
st.dataframe(df_stock)

# Plot the data
plot_data(df_exchange, df_stock)

# Alerts (optional)
threshold = 2  # Set a percentage threshold
if abs(df_exchange['Percentage Change'].iloc[-1]) > threshold:
    send_alert(f"Alert: Exchange rate change exceeded {threshold}%! Last change: {df_exchange['Percentage Change'].iloc[-1]}%")
