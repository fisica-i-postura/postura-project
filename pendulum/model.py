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

class JointPositions:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_joint_as_positions(joints, joint) -> JointPositions:
    return JointPositions(smooth(joints.get_group(joint)[X_POSITION_ABSOLUTE].to_numpy()),
                          smooth(joints.get_group(joint)[Y_POSITION_ABSOLUTE].to_numpy()))


def get_angle(fixed_points: JointPositions, moving_points: JointPositions) -> np.ndarray:
    x_diff = moving_points.x - fixed_points.x
    y_diff = moving_points.y - fixed_points.y
    return np.degrees(np.arctan2(x_diff, y_diff))


class Pendulum:
    def __init__(self, df: pd.DataFrame) -> None:
        joints = df[df[JOINT_ID].isin([RIGHT_SHOULDER, RIGHT_WRIST])].groupby(JOINT_ID)
        self.shoulder = get_joint_as_positions(joints, RIGHT_SHOULDER)
        self.wrist = get_joint_as_positions(joints, RIGHT_WRIST)
        self.angle = get_angle(self.shoulder, self.wrist)
        self.time = joints.get_group(RIGHT_SHOULDER)[SECOND].to_numpy()