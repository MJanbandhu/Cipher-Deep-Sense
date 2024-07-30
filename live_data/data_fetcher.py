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