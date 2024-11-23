from pathlib import Path

from plotly.io import write_image, write_html

from kinematic.joint_kinematics import JointKinematics
from plotting.plots import plot_helper


class KinematicsPlotHelper:
    def __init__(self, kinematics_data: JointKinematics, joint_name: str, path: Path) -> None:
        self.kinematics_data = kinematics_data
        self.joint_name = joint_name
        self.path = path

    def plot(self):
        self.plot_position()
        self.plot_velocity()
        self.plot_acceleration()

    def plot_position(self):
        names = ["x position", "y position"]

        ys = [self.kinematics_data.x_position, self.kinematics_data.y_position]
        fig = plot_helper(self.kinematics_data.t, ys, names, f"{self.joint_name}: Position vs Time", "Time (s)", "Position (m)", "lines")
        write_image(fig, f"{self.path}/{self.joint_name}_position.png")
        write_html(fig, f"{self.path}/{self.joint_name}_position.html")

        ys_smooth = [self.kinematics_data.x_position_smooth, self.kinematics_data.y_position_smooth]
        fig = plot_helper(self.kinematics_data.t, ys_smooth, names, f"{self.joint_name}: Position (smooth) vs Time", "Time (s)", "Position (m)", "lines")
        write_image(fig, f"{self.path}/{self.joint_name}_position_smooth.png")
        write_html(fig, f"{self.path}/{self.joint_name}_position_smooth.html")

    def plot_velocity(self):
        names = ["velocity", "x velocity", "y velocity"]

        ys = [self.kinematics_data.velocity, self.kinematics_data.x_velocity, self.kinematics_data.y_velocity]
        fig = plot_helper(self.kinematics_data.t, ys, names, f"{self.joint_name}: Velocity vs Time", "Time (s)", "Velocity (m/s)", "lines")
        write_image(fig, f"{self.path}/{self.joint_name}_velocity.png")
        write_html(fig, f"{self.path}/{self.joint_name}_velocity.html")

        ys_smooth = [self.kinematics_data.velocity_smooth, self.kinematics_data.x_velocity_smooth, self.kinematics_data.y_velocity_smooth]
        fig = plot_helper(self.kinematics_data.t, ys_smooth, names, f"{self.joint_name}: Velocity (smooth) vs Time", "Time (s)", "Velocity (m/s)", "lines")
        write_image(fig, f"{self.path}/{self.joint_name}_velocity_smooth.png")
        write_html(fig, f"{self.path}/{self.joint_name}_velocity_smooth.html")

    def plot_acceleration(self):
        names = ["acceleration", "x acceleration", "y acceleration"]

        ys = [self.kinematics_data.accel, self.kinematics_data.x_accel, self.kinematics_data.y_accel]
        fig = plot_helper(self.kinematics_data.t, ys, names, f"{self.joint_name}: Acceleration vs Time", "Time (s)", "Acceleration (m/s^2)", "lines")
        write_image(fig, f"{self.path}/{self.joint_name}_acceleration.png")
        write_html(fig, f"{self.path}/{self.joint_name}_acceleration.html")

        ys_smooth = [self.kinematics_data.accel_smooth, self.kinematics_data.x_accel_smooth, self.kinematics_data.y_accel_smooth]
        fig = plot_helper(self.kinematics_data.t, ys_smooth, names, f"{self.joint_name}: Acceleration (smooth) vs Time", "Time (s)", "Acceleration (m/s^2)", "lines")
        write_image(fig, f"{self.path}/{self.joint_name}_acceleration_smooth.png")
        write_html(fig, f"{self.path}/{self.joint_name}_acceleration_smooth.html")