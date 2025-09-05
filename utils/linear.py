def linear_interpolation(w0, w1, days=6):
    """
    Perform linear interpolation between two weights over a specified number of days.
    
    w0: initial weight
    w1: final weight
    days: number of days to interpolate
    
    returns: list of weights for each day
    """
    return [float(np.round(w0 + (w1 - w0) * i / days, 2)) for i in range(days + 1)]