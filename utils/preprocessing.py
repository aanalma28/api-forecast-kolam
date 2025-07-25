import logging
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

def preprocess_input_data(data):
    """Preprocess fish farming data for forecasting"""
    try:
        import numpy as np
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        
        # Extract target weight and sequence
        target_weight = float(data['target_weight'])
        sequence = data['sequence']
        
        # Convert sequence to DataFrame
        df = pd.DataFrame(sequence)
        
        # Add pool_type column (default to A1 if not provided)
        if 'pool_type' not in df.columns:
            df['pool_type'] = 'A1'
        
        # Fill missing fish_type with the most common one or default
        if 'fish_type' not in df.columns:
            df['fish_type'] = 'Nila'
        else:
            df['fish_type'] = df['fish_type'].fillna('Nila')
        
        # Transform dates
        df = transform_date(df)
        
        # Encode categorical variables
        df = encode_categorical_features(df)
        
        # Remove avg_weight and date columns
        columns_to_drop = ['avg_weight', 'date']
        df_processed = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        
        # Scale features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df_processed)
        
        # Create sequences with window size 7
        sequences = create_sequences(scaled_data, window_size=7)
        
        return {
            'target_weight': target_weight,
            'sequences': sequences,
            'scaler': scaler,
            'feature_columns': df_processed.columns.tolist(),
            'original_data': df,
            'processed_data': df_processed,
            'preprocessed_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error preprocessing fish farming data: {e}")
        raise ValueError(f"Failed to preprocess data: {str(e)}")

def transform_date(df):
    """Transform date column into multiple time features"""
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['week'] = df['date'].dt.isocalendar().week
    df['day_to'] = df['date'].dt.dayofyear
    return df

def encode_categorical_features(df):
    """Encode fish_type and pool_type using predefined categories"""
    df = df.copy()
    
    # Define valid categories
    fish_types = ["Nila", "Mujair", "Gurame"]
    pool_types = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
    
    # Encode fish_type
    from sklearn.preprocessing import LabelEncoder
    fish_encoder = LabelEncoder()
    fish_encoder.fit(fish_types)
    df['fish_type_encoded'] = fish_encoder.transform(df['fish_type'])
    
    # Encode pool_type
    pool_encoder = LabelEncoder()
    pool_encoder.fit(pool_types)
    df['pool_type_encoded'] = pool_encoder.transform(df['pool_type'])
    
    # Drop original categorical columns
    df = df.drop(columns=['fish_type', 'pool_type'])
    
    return df

def create_sequences(data, window_size=7):
    """Create sequences with specified window size"""
    import numpy as np
    
    if len(data) < window_size:
        raise ValueError(f"Data length ({len(data)}) is less than window size ({window_size})")
    
    sequences = []
    for i in range(len(data) - window_size + 1):
        sequence = data[i:i + window_size]
        sequences.append(sequence)
    
    # Convert to numpy array with shape (num_sequences, window_size, num_features)
    sequences = np.array(sequences)
    
    logger.info(f"Created sequences with shape: {sequences.shape}")
    
    return sequences

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
