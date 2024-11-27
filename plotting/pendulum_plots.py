from pathlib import Path

import numpy as np
from plotly.io import write_image, write_html

from pendulum.solid_bar_pendulum import SolidBarPendulum
from plotting.plots import plot_helper


class PendulumPlotHelper:
    def __init__(self, pendulum: SolidBarPendulum, steps, path: Path):
        self.pendulum = pendulum
        self.steps = steps
        self.path = path

    def plot(self):
        names = ["angle"]
        angle = np.degrees(np.arctan(np.tan(self.pendulum.angle)))
        ys = [angle]
        time = self.pendulum.pivot.t
        fig = plot_helper(time, ys, names, "Shoulder-Wrist angle vs Time", "Time (s)", "Angle (degrees)", steps=self.steps)
        write_image(fig, f"{self.path}/angle.png", width=1280, height=720, scale=4, engine="kaleido", format="png")
        write_html(fig, f"{self.path}/angle.html")
