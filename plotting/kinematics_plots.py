from pathlib import Path

import numpy as np
from plotly.io import write_image, write_html

from kinematic.joint_kinematics import JointKinematics
from plotting.plots import plot_helper


def export_fig_as_png(fig, path):
    write_image(fig, path, format="png", scale=4, width=1280, height=720)


class KinematicsPlotHelper:
    def __init__(self, kinematics_data: JointKinematics, joint_name: str, path: Path, steps: np.ndarray) -> None:
        self.kinematics_data = kinematics_data
        self.time = kinematics_data.t
        self.joint_name = joint_name
        self.path = path
        self.steps = steps

    def plot(self):
        self.plot_position()
        self.plot_velocity()
        self.plot_acceleration()

    def plot_position(self):
        names = ["x position", "x position (smooth)", "y position", "y position (smooth)"]
        ys = [self.kinematics_data.x_position, self.kinematics_data.x_position_smooth, self.kinematics_data.y_position, self.kinematics_data.y_position_smooth]
        fig = plot_helper(self.time, ys, names, f"{self.joint_name}: Position vs Time", "Time (s)", "Position (m)", "lines", self.steps)
        export_fig_as_png(fig, f"{self.path}/{self.joint_name}_position.png")
        write_html(fig, f"{self.path}/{self.joint_name}_position.html")

    def plot_velocity(self):
        names = ["x velocity", "x velocity (smooth)", "y velocity", "y velocity (smooth)", "velocity", "velocity (smooth)"]
        ys = [self.kinematics_data.x_velocity, self.kinematics_data.x_velocity_smooth, self.kinematics_data.y_velocity, self.kinematics_data.y_velocity_smooth, self.kinematics_data.velocity, self.kinematics_data.velocity_smooth]
        fig = plot_helper(self.time, ys, names, f"{self.joint_name}: Velocity vs Time", "Time (s)", "Velocity (m/s)", "lines", self.steps)
        export_fig_as_png(fig, f"{self.path}/{self.joint_name}_velocity.png")
        write_html(fig, f"{self.path}/{self.joint_name}_velocity.html")

    def plot_acceleration(self):
        names = ["x acceleration", "x acceleration (smooth)", "y acceleration", "y acceleration (smooth)", "acceleration", "acceleration (smooth)"]
        ys = [self.kinematics_data.x_accel, self.kinematics_data.x_accel_smooth, self.kinematics_data.y_accel, self.kinematics_data.y_accel_smooth, self.kinematics_data.accel, self.kinematics_data.accel_smooth]
        fig = plot_helper(self.time, ys, names, f"{self.joint_name}: Acceleration vs Time", "Time (s)", "Acceleration (m/s^2)", "lines", self.steps)
        export_fig_as_png(fig, f"{self.path}/{self.joint_name}_acceleration.png")
        write_html(fig, f"{self.path}/{self.joint_name}_acceleration.html")