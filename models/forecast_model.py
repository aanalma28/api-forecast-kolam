import os
import logging
import numpy as np
import pandas as pd
import joblib
from utils.preprocessing import preprocess_input_data
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class FishForecastModel:
    """Fish farming forecasting model placeholder - designed to work with user's own model"""
    
    def __init__(self, model_path='data/model_lstm.h5'):
        self.model = load_model(model_path)
        self.is_trained = True
        self.model_path = model_path
        logger.info("Fish forecasting model loaded from .h5 file.")
        
        # This is a placeholder - user will provide their own model
        logger.info("Fish forecasting model initialized. Waiting for user's model integration.")
    
    def predict_until_target(self, data):
        """
        Predict fish growth until target weight is reached
        This is a placeholder implementation - user should replace with their actual model
        """
        try:            
            # prepare the data
            sequence = data['sequence']            
            new_sequence = sequence.copy()  # to avoid modifying the original
            target_weight = float(data['target_weight'])

            # set current weight from last known sequence
            current_weight = new_sequence[-1]['avg_weight']
            week_age = new_sequence[-1]['week_age']
            
            predictions = []   
            day_counter = 1
            feature_columns = None
            sequences_shape = None
            
            # Simulate predictions until target is reached (max 365 days for safety)
            while current_weight < target_weight and day_counter <= 365:
                # predict next weight                
                input_seq = preprocess_input_data(new_sequence)
                feature_columns = input_seq['feature_columns']
                sequences_shape = input_seq['sequences'].shape
                next_pred = self.model.predict(input_seq['sequences'][-1][np.newaxis, ...])
                result_pred = input_seq['scaler_target'].inverse_transform(next_pred.reshape(1, -1))
                print(result_pred[0][0])

                # create new dict
                new_dict = {}
                new_dict['date'] = (datetime.strptime(new_sequence[-1]['date'], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                new_dict['fish_type'] = new_sequence[-1]['fish_type']
                new_dict['start_weight'] = new_sequence[-1]['start_weight']
                new_dict['avg_weight'] = float(result_pred[0][0])
                new_dict['week_age'] = week_age + (day_counter // 7) # floor division

                new_sequence.pop(0)  # remove the oldest entry
                new_sequence.append(new_dict)  # add the new prediction
                
                current_weight = result_pred[0][0]
                predictions.append({
                    'day': int(day_counter),
                    'predicted_weight': round(float(current_weight), 4),
                    'date': new_dict['date'],
                    'days_to_target': int(day_counter) if current_weight >= target_weight else None
                })
                
                day_counter += 1
            
            # Calculate summary
            final_prediction = predictions[-1] if predictions else None
            summary = {
                'days_to_reach_target': int(final_prediction['day']) if (final_prediction and final_prediction['predicted_weight'] >= target_weight) else None,
                'target_weight': float(target_weight),
                'current_weight': float(current_weight),
                'final_predicted_weight': float(final_prediction['predicted_weight']) if final_prediction else current_weight,
                'target_reached': bool(final_prediction['predicted_weight'] >= target_weight) if final_prediction else False,
                'total_predictions': int(len(predictions)),
            }
            
            return {
                'predictions': predictions,
                'summary': summary,
                'feature_columns': feature_columns,
                'sequences_shape': sequences_shape,
                'model_info': {
                    'model_type': 'Placeholder Fish Growth Model',
                    'note': 'Replace this with your actual trained model'
                }
            }
            
        except Exception as e:
            logger.error(f"Error in fish prediction: {e}")
            raise
    
    def _estimate_current_weight(self, sequences):
        """Estimate current weight from sequence data - placeholder logic"""
        # This is placeholder logic - replace with actual estimation
        if len(sequences) > 0 and sequences.shape[2] > 0:
            # Assume the last value in some feature represents weight-related info
            return 0.8  # Placeholder starting weight
        return 0.5
    
    def _calculate_growth_rate(self, sequences):
        """Calculate growth rate from sequences - placeholder logic"""
        # Placeholder growth calculation - replace with actual model prediction
        base_growth = 0.02  # 20g per day base growth
        variation = np.random.normal(0, 0.005)  # Add some variation
        return max(0, base_growth + variation)
    
    def get_model_info(self):
        """Get information about the current model"""
        return {
            'model_type': 'Fish Growth Forecasting Model',
            'is_trained': True,  # Placeholder - user's model should be pre-trained
            'input_shape': '(batch_size, 7, 21)',  # Expected input shape
            'output_type': 'Sequential weight predictions until target',
            'model_path': self.model_path,            
        }

# For backward compatibility
ForecastModel = FishForecastModel