import numpy as np
from datetime import datetime, timedelta
from utils.interpolations import cubic_spline_interpolation, exp_interpolation, linear_interpolation, log_interpolation, monotonic_interpolation, generate_sequences

def generate_sequences(start_weight, end_weight, data):
    start_weight = float(start_weight)
    end_weight = float(end_weight)
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    target_weight = float(data.get('target_weight'))
    percentage = np.round(end_weight / start_weight, 2)
    known_times = [np.datetime64(start_date), np.datetime64(end_date)]
    known_values = np.array([start_weight, end_weight])
    weights = []

    if percentage < 0.6:
        weights = exp_interpolation(start_weight, end_weight)
    elif 0.6 <= percentage < 0.8:
        weights = monotonic_interpolation(known_times, known_values)
    elif 0.8 <= percentage < 1.0:
        weights = log_interpolation(start_weight, end_weight, K=target_weight)

