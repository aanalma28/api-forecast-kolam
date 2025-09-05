import scipy.interpolate import PchipInterpolator
import numpy as np

def monotonic_interpolation(known_times, known_values):
    """
    Perform monotonic interpolation using PCHIP (Piecewise Cubic Hermite Interpolating Polynomial).
    
    known_times: array-like, times at which known values are provided, exp: [0, 7, 14, 21] example each week
    known_values: array-like, values corresponding to the known times exp: [10, 12, 15, 20] example weight fish
    
    returns: function that can be used to interpolate values at new times
    """
    pchip = PchipInterpolator(known_times, known_values, extrapolate=False)
    daily = pchip(np.arrange(0, max(known_times)+1))
    return daily
