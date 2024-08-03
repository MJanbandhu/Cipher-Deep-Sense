# live_data/data_fetcher.py

import requests
import pandas as pd

API_KEY = 'your_api_key'
BASE_URL = 'https://www.alphavantage.co/query'

def fetch_real_time_data(symbol):
    """Fetch real-time data from Alpha Vantage."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    df = pd.DataFrame(data['Time Series (1min)']).T
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    return df

if __name__ == "__main__":
    symbol = 'AAPL'
    data = fetch_real_time_data(symbol)
    print(data.head())


import requests
import pandas as pd
from datetime import datetime
from db_connector import insert_stock_data

# Replace with your data provider's API endpoint and API key
API_ENDPOINT = 'https://api.example.com/live_stock_data'
API_KEY = 'your_api_key'

def fetch_live_data():
    response = requests.get(API_ENDPOINT, headers={'Authorization': f'Bearer {API_KEY}'})
    data = response.json()

    # Assuming the data comes in JSON format
    stock_data = pd.DataFrame(data)
    stock_data['timestamp'] = datetime.utcnow()

    # Insert fetched data into the database
    insert_stock_data(stock_data)

if __name__ == "__main__":
    fetch_live_data()