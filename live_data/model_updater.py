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




def update_model(model, new_data):
    # Implement logic for updating and securing models
    pass


from scripts.ann_model import train_ann_model
from scripts.logistic_regression import train_logistic_model
from scripts.decision_tree import train_decision_tree_model
from scripts.random_forest import train_random_forest_model
from scripts.svm_model import train_svm_model
from db_connector import create_connection, insert_model_predictions

def update_models():
    """Retrain models with the latest data."""
    connection = create_connection()
    if connection is not None:
        query = "SELECT * FROM stock_data ORDER BY timestamp DESC LIMIT 1000"
        df = pd.read_sql(query, connection)
        connection.close()

        # Retrain models with the latest data
        ann_model = train_ann_model(df)
        logistic_model = train_logistic_model(df)
        decision_tree_model = train_decision_tree_model(df)
        random_forest_model = train_random_forest_model(df)
        svm_model = train_svm_model(df)

        # Save models to the disk
        ann_model.save('../models/ann_model.h5')
        logistic_model.save('../models/logistic_model.pkl')
        decision_tree_model.save('../models/decision_tree_model.pkl')
        random_forest_model.save('../models/random_forest_model.pkl')
        svm_model.save('../models/svm_model.pkl')

        # Predict and insert into the database
        predictions = {
            'timestamp': pd.to_datetime('now'),
            'ann_prediction': ann_model.predict(df),
            'logistic_regression_prediction': logistic_model.predict(df),
            'decision_tree_prediction': decision_tree_model.predict(df),
            'random_forest_prediction': random_forest_model.predict(df),
            'svm_prediction': svm_model.predict(df)
        }
        insert_model_predictions(pd.DataFrame([predictions]))

if __name__ == "__main__":
    update_models()
