import numpy as np
from scipy import constants as const

from kinematic.joint_kinematics import JointKinematics


def get_angle_np(fixed_points: np.ndarray, moving_points: np.ndarray) -> np.ndarray:
    xs_diff = moving_points[0] - fixed_points[0]
    ys_diff = moving_points[1] - fixed_points[1]
    return np.arctan2(xs_diff, -ys_diff)


class SolidBarPendulum:
    def __init__(self, pivot: JointKinematics, center_of_mass: JointKinematics, solid_bar_end: JointKinematics, mass: float):
        self.pivot = pivot
        self.center_of_mass = center_of_mass
        self.length = solid_bar_end
        self.mass = mass
        pivot_xy = np.array([pivot.x_position_smooth, pivot.y_position_smooth])
        center_of_mass_xy = np.array([center_of_mass.x_position_smooth, center_of_mass.y_position_smooth])
        self.angle = get_angle_np(pivot_xy, center_of_mass_xy)
        self.angular_velocity = np.full(len(pivot.t), np.nan)
        self.angular_velocity[1:] = np.diff(self.angle) / np.diff(pivot.t)
        self.center_of_mass_to_pivot_distance = np.linalg.norm(pivot_xy - center_of_mass_xy, axis=0)
        self.moment_of_inertia = mass * self.center_of_mass_to_pivot_distance**2 / 3
        self.angular_frequency = (mass * const.g * self.center_of_mass_to_pivot_distance / self.moment_of_inertia) ** 0.5
        self.period = 2 * const.pi / self.angular_frequency
