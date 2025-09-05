import numpy as np
from utils.exp_interpolation import exp_interpolation
a = np.array([12, 15])
result = exp_interpolation(a[0], a[1])
print(result)  