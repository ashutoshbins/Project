import yfinance as yf

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

# Instantiate and use the toolkit
stock_toolkit = StockPriceToolkit()
stock_prices = stock_toolkit.get_stock_prices()
print(stock_prices)
