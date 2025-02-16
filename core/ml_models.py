# core/ml_models.py

import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.preprocessing import MinMaxScaler

class MLModels:
    def __init__(self, data):
        self.data = data
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def _validate_data(self):
        """Ensure data has 'close' column and sufficient length"""
        if 'close' not in self.data.columns:
            raise ValueError("Data must contain 'close' column")
        if len(self.data) < 100:
            raise ValueError("Need at least 100 data points")

    def preprocess_data(self, window_size=60):
        """Convert raw data to ML-friendly format"""
        self._validate_data()
        
        scaled_data = self.scaler.fit_transform(
            self.data['close'].values.reshape(-1, 1)
        )
        
        X, y = [], []
        for i in range(window_size, len(scaled_data)):
            X.append(scaled_data[i-window_size:i, 0])
            y.append(scaled_data[i, 0])
            
        return np.array(X), np.array(y)

    def train_model(self):
        """Train an XGBoost model"""
        X, y = self.preprocess_data()
        model = XGBRegressor(n_estimators=200, learning_rate=0.1)
        model.fit(X, y)
        return model

    def predict_future(self, model, steps=10):
        """Generate future predictions"""
        last_sequence = self.data['close'].values[-60:]
        scaled_sequence = self.scaler.transform(last_sequence.reshape(-1, 1))
        
        predictions = []
        for _ in range(steps):
            x_input = scaled_sequence.reshape(1, -1)
            pred = model.predict(x_input)[0]
            predictions.append(pred)
            scaled_sequence = np.append(scaled_sequence[1:], [[pred]])
            
        return self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))