import numpy as np

def resultant(x: np.ndarray, y: np.ndarray):
    return np.sqrt(np.square(x) + np.square(y))

def direction(x: np.ndarray, y: np.ndarray):
    """Returns the angle in radians"""
    return np.arctan(x, y)

def variation(x: np.ndarray, y: np.ndarray):
    assert x.shape == y.shape
    variation_yx = np.diff(y) / np.diff(x)
    values = np.full_like(x, np.nan)
    values[1:] = variation_yx
    return values