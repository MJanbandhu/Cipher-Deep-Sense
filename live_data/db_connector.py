# live_data/db_connector.py

from sqlalchemy import create_engine
import pandas as pd

def connect_db():
    """Connect to the MySQL database."""
    engine = create_engine('mysql+pymysql://username:password@localhost/stock_db')
    return engine

def store_data(df, table_name):
    """Store data in the specified table."""
    engine = connect_db()
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

if __name__ == "__main__":
    data = pd.DataFrame({'date': ['2024-07-30'], 'price': [100]})
    store_data(data, 'stock_prices')