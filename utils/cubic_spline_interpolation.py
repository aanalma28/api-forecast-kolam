from scipy.interpolate import CubicSpline
import numpy as np

def cubic_spline_interpolation(w_start, w_end, days=6):
    """
    This function performs cubic spline interpolation between two weights over a specified number of days.
    
    Parameters:
    w_start (float): Initial weight.
    w_end (float): Final weight.
    days (int): Number of days to interpolate (default is 6).
    
    Returns:
    list: A list of interpolated weights for each day.
    """
    x = [0, days]
    y = [w_start, w_end]
    
    cs = CubicSpline(x, y)
    
    return [float(np.round(cs(i), 2)) for i in range(0, days + 1)]