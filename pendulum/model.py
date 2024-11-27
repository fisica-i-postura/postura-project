import numpy as np
import pandas as pd

from kinematic.dataset_smoothing import smooth
from constants.df_columns_names import JOINT_ID, X_POSITION_ABSOLUTE, Y_POSITION_ABSOLUTE, SECOND

RIGHT_SHOULDER = 12
RIGHT_WRIST = 16

"""
take two joints, such as the shoulder and elbow, and calculate the angle between them.
The angle is calculated with respect to the vertical line that passes through the shoulder.
The angle is calculated using the arctangent function.
"""

class JointPoints:
    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def __sub__(self, other) -> np.ndarray:
        return np.array([self.xs - other.xs, self.ys - other.ys])


def get_joint_as_positions(joints, joint) -> JointPoints:
    xs = smooth(joints.get_group(joint)[X_POSITION_ABSOLUTE].to_numpy())
    ys = smooth(joints.get_group(joint)[Y_POSITION_ABSOLUTE].to_numpy())
    return JointPoints(xs, ys)


def get_angle(fixed_points: JointPoints, moving_points: JointPoints) -> np.ndarray:
    xs_diff = moving_points.xs - fixed_points.xs
    ys_diff = moving_points.ys - fixed_points.ys
    return np.degrees(np.arctan(xs_diff, ys_diff))


class Pendulum:
    def __init__(self, df: pd.DataFrame) -> None:
        joints = df[df[JOINT_ID].isin([RIGHT_SHOULDER, RIGHT_WRIST])].groupby(JOINT_ID)
        self.shoulder = get_joint_as_positions(joints, RIGHT_SHOULDER)
        self.wrist = get_joint_as_positions(joints, RIGHT_WRIST)
        self.angle = get_angle(self.shoulder, self.wrist)
        self.time = joints.get_group(RIGHT_SHOULDER)[SECOND].to_numpy()