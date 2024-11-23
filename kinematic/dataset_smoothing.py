import numpy as np
from scipy.signal import savgol_filter

def smooth(dataset: np.ndarray):
    """Smooths the dataset using Savitzky-Golay filter"""
    window_length = min(27, len(dataset))
    return savgol_filter(dataset, window_length=window_length, polyorder=3)