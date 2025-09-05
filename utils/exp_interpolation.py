import numpy as np

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