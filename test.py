import numpy as np
from datetime import datetime
from utils.interpolations import exp_interpolation, monotonic_interpolation, log_interpolation
a = np.array([12, 15])
result = exp_interpolation(a[0], a[1])
print(result)

tgl = np.array(['2024-01-19', '2024-01-25'], dtype='datetime64[D]')
day = tgl.astype('datetime64[D]').astype(object)
known_values = np.array([0.22, 0.25])
known_times = [d.day for d in day]
result_mono = monotonic_interpolation(known_times, known_values)
print(result_mono)