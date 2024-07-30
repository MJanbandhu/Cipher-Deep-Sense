# live_data/model_updater.py

from keras.models import load_model
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from db_connector import connect_db

def load_data():
    """Load new data for training."""
    engine = connect_db()
    query = "SELECT * FROM stock_prices ORDER BY date DESC LIMIT 1000"
    data = pd.read_sql(query, con=engine)
    return data

def update_model():
    """Update the model with new data."""
    model = load_model('../models/lstm_model.h5')
    new_data = load_data()
    scaler = MinMaxScaler()
    new_data_scaled = scaler.fit_transform(new_data['price'].values.reshape(-1, 1))
    X_train = new_data_scaled[:-1]
    y_train = new_data_scaled[1:]

    model.fit(X_train, y_train, epochs=1, batch_size=1)
    model.save('../models/lstm_model.h5')

if __name__ == "__main__":
    update_model()