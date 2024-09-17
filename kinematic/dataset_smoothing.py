import numpy as np
from scipy.signal import savgol_filter

def smooth(dataset: np.ndarray):
    return savgol_filter(dataset, window_length=11, polyorder=3)