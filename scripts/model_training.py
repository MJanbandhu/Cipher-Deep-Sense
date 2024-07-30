# scripts/model_training.py

from keras.models import Sequential
from keras.layers import Dense, LSTM
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def train_model(df):
    """Train an LSTM model for stock prediction."""
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[['close']])
    
    X, y = [], []
    for i in range(len(df_scaled) - 1):
        X.append(df_scaled[i])
        y.append(df_scaled[i + 1])
    
    X, y = np.array(X), np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    model.fit(X_train, y_train, epochs=10, batch_size=32)
    model.save('../models/lstm_model.h5')

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    train_model(df)