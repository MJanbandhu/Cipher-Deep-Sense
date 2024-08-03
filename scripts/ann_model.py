# scripts/ann_model.py

from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def train_ann(df):
    """Train an ANN model for stock prediction."""
    X = df[['open', 'high', 'low', 'volume']]
    y = df['close']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=0)
    
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    model.fit(X_train, y_train, epochs=10, batch_size=32)
    model.save('../models/ann_model.h5')

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/stock_data_features.csv')
    train_ann(df)



# scripts/ann_model.py
def predict_ann(df, model):
    # Preprocess df as needed for the model
    X = df[['feature1', 'feature2', ...]].values
    predictions = model.predict(X)
    return predictions