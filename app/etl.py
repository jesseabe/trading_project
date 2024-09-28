import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os


def download_and_process_data(ticker, yahoo_ticker, start_date, end_date, interval):
    # Download the data
    data = yf.download(tickers=yahoo_ticker, start=start_date, end=end_date, interval=interval)
    
    # Add the ticker column
    data['Ticker'] = ticker
    
    # Add the variation column
    data['Oscillation'] = data['High'] - data['Low']

    data = data.reset_index()
    
    return data

# Define parameters
end_date = datetime.today()
start_date = end_date - timedelta(days=360)
interval = '1D'

# Download and process data for each ticker
ibov = download_and_process_data("WINFUT", "^BVSP", start_date, end_date, interval)
print(ibov.head())
print(ibov.columns)

# Connect to the database
load_dotenv(".env")
try:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    dbname = os.getenv("POSTGRES_DB")

    # Create connection
    connect = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        dbname=dbname
    )

    # Creating a cursor object
    cursor = connect.cursor()
    connect.autocommit = True

    # Create the table if it doesn't exist
    sql = (
    """
    CREATE TABLE IF NOT EXISTS ibov (
        date DATE PRIMARY KEY,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume FLOAT,
        ticker VARCHAR,
        oscillation FLOAT
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
            (row['Date'].strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Ticker'], row['Oscillation'])
        )
    connect.commit()

    print("Data inserted successfully!")
except (Exception, Error) as error:
    print("Error while interacting with PostgreSQL", error)
finally:
    if connect:
        cursor.close()
        connect.close()
