# scripts/feature_engineering.py

import pandas as pd

def create_features(df):
    """Create new features for stock data."""
    df['price_diff'] = df['close'] - df['open']
    df['rolling_mean'] = df['close'].rolling(window=5).mean()
    return df

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/stock_data_processed.csv')
    df_features = create_features(df)
    df_features.to_csv('../data/processed/stock_data_features.csv', index=False)