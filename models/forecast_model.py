import os
import logging
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class ForecastModel:
    """Simple time series forecasting model using linear regression with trend and seasonality features"""
    
    def __init__(self, model_path='data/sample_model.pkl'):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = model_path
        self.feature_names = ['trend', 'sin_seasonal', 'cos_seasonal', 'month', 'day_of_week']
        
        # Try to load existing model
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing model or create a new one"""
        try:
            if os.path.exists(self.model_path):
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.is_trained = True
                logger.info("Model loaded successfully from disk")
            else:
                self._create_sample_model()
                logger.info("Created new sample model")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self._create_sample_model()
    
    def _create_sample_model(self):
        """Create and train a sample model with synthetic data"""
        try:
            # Create sample training data
            dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
            np.random.seed(42)
            
            # Generate synthetic time series with trend and seasonality
            trend = np.linspace(100, 200, len(dates))
            seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
            noise = np.random.normal(0, 10, len(dates))
            values = trend + seasonal + noise
            
            df = pd.DataFrame({
                'date': dates,
                'value': values
            })
            
            # Train the model
            self._train_model(df)
            
            # Save the model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, self.model_path)
            
            logger.info("Sample model created and saved successfully")
            
        except Exception as e:
            logger.error(f"Error creating sample model: {e}")
            # Create a minimal fallback model
            self.model = LinearRegression()
            self.is_trained = False
    
    def _extract_features(self, df):
        """Extract features from datetime for forecasting"""
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        # Trend feature (days since start)
        start_date = df['date'].min()
        df['trend'] = (df['date'] - start_date).dt.days
        
        # Seasonal features
        day_of_year = df['date'].dt.dayofyear
        df['sin_seasonal'] = np.sin(2 * np.pi * day_of_year / 365.25)
        df['cos_seasonal'] = np.cos(2 * np.pi * day_of_year / 365.25)
        
        # Calendar features
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        
        return df[self.feature_names]
    
    def _train_model(self, df):
        """Train the forecasting model"""
        try:
            # Extract features
            X = self._extract_features(df)
            y = df['value'].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model = LinearRegression()
            self.model.fit(X_scaled, y)
            self.is_trained = True
            
            # Calculate training metrics
            y_pred = self.model.predict(X_scaled)
            mae = mean_absolute_error(y, y_pred)
            mse = mean_squared_error(y, y_pred)
            
            logger.info(f"Model trained successfully. MAE: {mae:.2f}, MSE: {mse:.2f}")
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def predict(self, start_date, periods=30):
        """Make forecasting predictions"""
        try:
            if not self.is_trained:
                raise ValueError("Model is not trained")
            
            # Generate future dates
            start_date = pd.to_datetime(start_date)
            future_dates = pd.date_range(start=start_date, periods=periods, freq='D')
            
            # Create DataFrame for prediction
            df_future = pd.DataFrame({'date': future_dates})
            
            # Extract features
            X_future = self._extract_features(df_future)
            X_future_scaled = self.scaler.transform(X_future)
            
            # Make predictions
            predictions = self.model.predict(X_future_scaled)
            
            # Format results
            results = []
            for i, (date, pred) in enumerate(zip(future_dates, predictions)):
                results.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'predicted_value': float(pred),
                    'period': i + 1
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise
    
    def get_model_info(self):
        """Get information about the current model"""
        return {
            'model_type': 'Linear Regression with Time Features',
            'is_trained': self.is_trained,
            'features': self.feature_names,
            'model_path': self.model_path
        }
