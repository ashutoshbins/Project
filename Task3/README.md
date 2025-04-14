## Currency Impact Analyzer for IT Companies

### Overview
The **Currency Impact Analyzer for IT Companies** is a tool designed to track daily exchange rates for multiple currencies (e.g., USD/INR, EUR/INR, JPY/INR, CHF/INR) and compare these movements against the stock performance of leading IT companies. This tool allows users to visualize how currency fluctuations impact stock prices, providing valuable insights for making informed investment decisions.

### Key Features:
- **Data Retrieval**: Fetches real-time exchange rates for various currencies (USD/INR, EUR/INR, JPY/INR, CHF/INR, etc.) and stock prices of leading IT companies using APIs such as **Yahoo Finance** or official data from sources like the **Reserve Bank of India (RBI)**.
- **Simple Analysis**: Calculates daily percentage changes in both currency exchange rates and stock prices, plotting trends side-by-side for easy visual correlation.
- **Alert System**: Optionally, set up thresholds that trigger email or message alerts when exchange rate movements exceed a set percentage, keeping users informed in real-time.

### Financial Importance:
- **Revenue Sensitivity**: Many Indian IT companies generate substantial revenue in foreign currencies, especially USD. As a result, fluctuations in exchange rates can significantly affect their profitability and margins. This tool provides a means of tracking and understanding this impact.
- **Investment Decisions**: By offering quick insights into how currency trends align with stock movements, the tool helps investors anticipate the effects of currency fluctuations on earnings and stock valuations, aiding more informed investment choices.

### Technology Stack:
- **Data Retrieval**: Fetch exchange rate and stock data using APIs such as **Yahoo Finance** or **RBI** data sources.
- **Analysis & Visualization**: Calculate percentage changes and plot trends using libraries like **Pandas** and **Matplotlib** for easy comparison.
- **Alerts**: Implement email or message alerts using libraries such as **smtplib** (for email) or **Twilio** (for SMS), ensuring users are notified when exchange rate movements exceed predefined thresholds.

This project aims to provide IT companies, investors, and analysts with a powerful tool to track currency fluctuations and their impact on stock performance, offering a more precise understanding of the relationship between forex movements and company valuations.
