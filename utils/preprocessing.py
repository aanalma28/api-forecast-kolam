import logging
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

def preprocess_input_data(data):
    """Preprocess and normalize input data for forecasting"""
    try:
        processed = {}
        
        # Handle start_date
        start_date = data.get('start_date')
        if start_date:
            processed['start_date'] = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        else:
            processed['start_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Handle periods
        periods = data.get('periods', 30)
        try:
            processed['periods'] = int(periods)
        except (ValueError, TypeError):
            processed['periods'] = 30
        
        # Ensure periods is within valid range
        processed['periods'] = max(1, min(365, processed['periods']))
        
        # Handle confidence level
        confidence_level = data.get('confidence_level', 0.95)
        try:
            processed['confidence_level'] = float(confidence_level)
        except (ValueError, TypeError):
            processed['confidence_level'] = 0.95
        
        # Ensure confidence level is within valid range
        processed['confidence_level'] = max(0.5, min(0.99, processed['confidence_level']))
        
        # Handle model parameters
        model_params = data.get('model_params', {})
        if isinstance(model_params, dict):
            processed['model_params'] = model_params
        else:
            processed['model_params'] = {}
        
        # Add metadata
        processed['preprocessed_at'] = datetime.now().isoformat()
        
        logger.debug(f"Preprocessed input data: {processed}")
        
        return processed
        
    except Exception as e:
        logger.error(f"Error preprocessing input data: {e}")
        # Return safe defaults
        return {
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'periods': 30,
            'confidence_level': 0.95,
            'model_params': {},
            'preprocessed_at': datetime.now().isoformat()
        }

def normalize_time_series_data(data):
    """Normalize time series data for model input"""
    try:
        if isinstance(data, list):
            # Convert list to pandas Series
            series = pd.Series(data)
        elif isinstance(data, dict):
            # Convert dict with date keys to pandas Series
            dates = pd.to_datetime(list(data.keys()))
            values = list(data.values())
            series = pd.Series(values, index=dates)
        else:
            raise ValueError("Unsupported data format")
        
        # Remove any infinite or NaN values
        series = series.replace([float('inf'), float('-inf')], None)
        series = series.dropna()
        
        # Basic outlier detection and capping
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        series = series.clip(lower=lower_bound, upper=upper_bound)
        
        return series
        
    except Exception as e:
        logger.error(f"Error normalizing time series data: {e}")
        return None

def validate_and_clean_features(features):
    """Validate and clean feature data"""
    try:
        cleaned_features = {}
        
        for key, value in features.items():
            if isinstance(value, (int, float)) and not pd.isna(value):
                cleaned_features[key] = float(value)
            elif isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                cleaned_features[key] = float(value)
        
        return cleaned_features
        
    except Exception as e:
        logger.error(f"Error cleaning features: {e}")
        return {}
