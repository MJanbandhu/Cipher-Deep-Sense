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



import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='stock_prediction_db',
            user='your_username',
            password='your_password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_stock_data(df):
    """Insert stock data into the database."""
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO stock_data (timestamp, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['timestamp'], row['open'], row['high'], row['low'], row['close'], row['volume']))
        connection.commit()
        cursor.close()
        connection.close()

def insert_model_predictions(df):
    """Insert model predictions into the database."""
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO model_predictions (timestamp, ann_prediction, logistic_regression_prediction, decision_tree_prediction, random_forest_prediction, svm_prediction)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['timestamp'], row['ann_prediction'], row['logistic_regression_prediction'], row['decision_tree_prediction'], row['random_forest_prediction'], row['svm_prediction']))
        connection.commit()
        cursor.close()
        connection.close()
