import numpy as np

def variation(x: np.ndarray, y: np.ndarray):
    assert x.shape == y.shape and len(x) == len(y)
    variation = [(yf - yi) / (xf - xi) for xi, xf, yi, yf in zip(x[:-1], x[1:], y[:-1], y[1:])]
    template = np.zeros_like(x)
    # print(f'Input len: {len(x)} ; Output len: {len(variation)}')
    template[-len(variation):] = variation
    return template