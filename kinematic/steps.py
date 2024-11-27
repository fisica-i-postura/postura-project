import numpy as np
from scipy.signal import find_peaks, savgol_filter

class StepsCalculator:
    def __init__(self, heel_y_position: np.ndarray):
        self.heel_y_position = savgol_filter(heel_y_position, 51, 3)
        self.maxima_indices, _ = find_peaks(self.heel_y_position)
        self.minima_indices, _ = find_peaks(-self.heel_y_position)

    def find_steps(self):
        self.filter_maxima()
        steps = []
        for m1, m2 in zip(self.maxima_indices[:-1], self.maxima_indices[1:]):
            min_idx = self.find_minima_between_maxima(m1, m2)
            if min_idx is not None:
                print(f"Step detected between {m1} and {m2} at {min_idx}")
                steps.append(min_idx)
        return np.array(steps)

    def filter_maxima(self):
        print(f"Maxima indices (before): {self.maxima_indices}")
        max_values = self.heel_y_position[self.maxima_indices]
        p90 = np.percentile(max_values, 60)

        maxima = [maxima for maxima in self.maxima_indices if p90 < self.heel_y_position[maxima]]
        self.maxima_indices = np.array([0] + maxima + [len(self.heel_y_position) - 1])
        print(f"Maxima indices (after): {self.maxima_indices}")

    def find_minima_between_maxima(self, m1, m2):
        minima = [minima for minima in self.minima_indices if m1 < minima < m2]
        return min(minima, key=lambda x: self.heel_y_position[x], default=None)
