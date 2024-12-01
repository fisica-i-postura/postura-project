from pathlib import Path

import numpy as np
from plotly.io import write_image, write_html

from pendulum.energy import Energy
from plotting.plots import plot_helper


class EnergyPlotHelper:
    def __init__(self, energy_data: Energy, steps, path: Path) -> None:
        self.energy_data = energy_data
        self.steps = steps
        self.path = path

    def plot(self):
        names = ["kinetic energy", "potential energy", "mechanical energy"]
        ys = [self.energy_data.kinetic_energy, self.energy_data.potential_energy, self.energy_data.mechanical_energy]
        fig = plot_helper(self.energy_data.time, ys, names, "Energy vs Time", "Time (s)", "Energy (J)", "lines", self.steps)
        write_image(fig, f"{self.path}/energy_plot.png")
        write_html(fig, f"{self.path}/energy_plot.html")

        names = ["work", "non-conservative forces work", "total work", "non-conservative forces total work"]
        x = self.energy_data.time
        total_work = np.full_like(x, self.energy_data.total_work)
        total_non_conservative_forces_work = np.full_like(x, self.energy_data.total_non_conservative_forces_work)
        ys = [self.energy_data.work, self.energy_data.non_conservative_forces_work, total_work, total_non_conservative_forces_work]
        fig = plot_helper(x, ys, names, "Work vs Time", "Time (s)", "Work (J)", "lines", self.steps)
        write_image(fig, f"{self.path}/work_plot.png")
        write_html(fig, f"{self.path}/work_plot.html")