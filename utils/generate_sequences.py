import numpy as np
from datetime import datetime, timedelta
from utils.interpolations import cubic_spline_interpolation, exp_interpolation, linear_interpolation, log_interpolation, monotonic_interpolation

def generate_sequences(data):
    initial_weight = float(data.get('initial_weight'))
    start_weight = float(data.get('start_weight'))
    end_weight = float(data.get('end_weight'))
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    target_weight = float(data.get('target_weight'))
    percentage = np.round(end_weight / start_weight, 2)
    known_times = [np.datetime64(start_date), np.datetime64(end_date)]
    known_values = np.array([start_weight, end_weight])
    weights = []
    sequences = []

    # Kenaikan berat
    if percentage > 1:
        if percentage <= 1.1:
            weights = linear_interpolation(start_weight, end_weight)            
        elif percentage <= 1.3:
            weights = exp_interpolation(start_weight, end_weight)            
        else:
            weights = log_interpolation(start_weight, end_weight, K=target_weight)            
    # Penurunan berat
    else:
        if percentage >= 0.9:
            weights = linear_interpolation(start_weight, end_weight)            
        elif percentage >= 0.7:
            weights = exp_interpolation(start_weight, end_weight)            
        else:
            weights = log_interpolation(start_weight, end_weight, K=target_weight)            

    for index, weight in enumerate(weights):
        date = (np.datetime64(start_date) + np.timedelta64(index, 'D')).astype(object)
        if weight > target_weight:
            break
        sequences.append({
            'date': str(date),
            'fish_type': data.get('fish_type'),
            'start_weight': float(np.round(initial_weight, 2)),
            'avg_weight': float(np.round(weight, 2)),
            'week_age': data.get('week_age')
        })
    
    return sequences
