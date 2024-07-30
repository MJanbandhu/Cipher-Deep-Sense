# scripts/data_preprocessing.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(df):
    """Clean and preprocess stock data."""
    df = df.dropna()
    scaler = MinMaxScaler()
    df[['open', 'high', 'low', 'close', 'volume']] = scaler.fit_transform(df[['open', 'high', 'low', 'close', 'volume']])
    return df

if __name__ == "__main__":
    df = pd.read_csv('../data/raw/stock_data.csv')
    df_processed = preprocess_data(df)
    df_processed.to_csv('../data/processed/stock_data_processed.csv', index=False)
