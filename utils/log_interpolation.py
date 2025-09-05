import numpy as np

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