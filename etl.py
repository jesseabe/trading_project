import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def download_and_process_data(ticker, yahoo_ticker, start_date, end_date, interval):
    # Download the data
    data = yf.download(tickers=yahoo_ticker, start=start_date, end=end_date, interval=interval)
    
    # Add the ticker column
    data['Ticker'] = ticker
    
    # Add the variation column
    data['Oscillation'] = data['High'] - data['Low']
    
    return data

# Define parameters
end_date = datetime.today()
start_date = end_date - timedelta(days=30)
interval = '15m'

# Download and process data for each ticker
petr = download_and_process_data("PETR4", "PETR4.SA", start_date, end_date, interval)
vale = download_and_process_data("VALE3", "VALE", start_date, end_date, interval)
ibov = download_and_process_data("WINFUT", "^BVSP", start_date, end_date, interval)
