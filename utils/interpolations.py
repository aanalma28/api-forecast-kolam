from scipy.interpolate import CubicSpline, PchipInterpolator
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


def exp_interpolation(w0, w1, days=6, exp=1e-9):
    """
    This formula is meant to be used for exponential interpolation within 1 week
    w0: initial weight
    w1: final weight
    days: number of days to interpolate
    exp: minimum weight to avoid division by zero
    returns: list of weights for each day    
    """
    w0 = max(w0, exp)    
    w1 = max(w1, exp)
    m = (w1 / w0) ** (1 / days)
    return [float(np.round(w0 * m ** i, 2)) for i in range(0, days + 1)]

def linear_interpolation(w0, w1, days=6):
    """
    Perform linear interpolation between two weights over a specified number of days.
    
    w0: initial weight
    w1: final weight
    days: number of days to interpolate
    
    returns: list of weights for each day
    """
    return [float(np.round(w0 + (w1 - w0) * i / days, 2)) for i in range(days + 1)]


def log_interpolation(y0, y_end, K, days=6, exp=1e-9):
    """
    Perform logarithmic interpolation between two weights over a specified number of days.
    
    y0: initial weight
    y_end: final weight
    K: scaling factor for the logarithmic interpolation exp: max_weight of fish
    days: number of days to interpolate
    exp: minimum weight to avoid division by zero
    
    returns: list of weights for each day
    """
    y0 = max(y0, exp)
    y_end = max(y_end, exp)
    
    if y0 >= K or y_end >= K:
        raise ValueError("y0 or y_end must be < K for logarithmic interpolation.")
    
    A = np.log((K / y0) - 1.0)
    B = np.log((K / y_end) - 1.0)
    r = (A - B) / float(days)

    if abs(r) < 1e-12: r = 1e-6
    t0 = A/r
    
    def y(t):
        return K / (1.0 + np.exp(-r * (t - t0)))
    return [float(np.round(y(i), 6)) for i in range(0, days + 1)]


def monotonic_interpolation(known_times, known_values):
    """
    Perform monotonic interpolation using PCHIP (Piecewise Cubic Hermite Interpolating Polynomial).
    
    known_times: array-like, times at which known values are provided, exp: [0, 7, 14, 21] example each week
    known_values: array-like, values corresponding to the known times exp: [10, 12, 15, 20] example weight fish
    
    returns: function that can be used to interpolate values at new times
    """    
    pchip = PchipInterpolator(known_times, known_values, extrapolate=False)
    daily = np.round(pchip(np.arange(known_times[0], max(known_times)+1)), 3)
    return daily