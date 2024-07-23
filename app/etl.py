import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import psycopg2
from psycopg2 import Error

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
start_date = end_date - timedelta(days=220)
interval = '1D'

# Download and process data for each ticker
ibov = download_and_process_data("WINFUT", "^BVSP", start_date, end_date, interval)

# Connect to the database
connect = psycopg2.connect( 
    user="postgres", 
    password="password", 
    host="localhost", 
    port="5432", 
    database="mydb"
)

# Creating a cursor object
cursor = connect.cursor()
connect.autocommit = True

# Create the table if it doesn't exist
sql = (
"""
CREATE TABLE IF NOT EXISTS ibov (
    Date DATE PRIMARY KEY,
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Volume FLOAT,
    Ticker VARCHAR,
    Oscillation FLOAT
);
"""
)
cursor.execute(sql)
connect.commit()

# Insert data into the table
for i, row in ibov.iterrows():
    cursor.execute(
        "INSERT INTO ibov (Date, Open, High, Low, Close, Volume, Ticker, Oscillation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (Date) DO NOTHING;",
        (i, row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Ticker'], row['Oscillation'])
    )
connect.commit()

print("Data inserted successfully!")
cursor.close()
connect.close()
