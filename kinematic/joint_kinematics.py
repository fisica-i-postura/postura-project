from kinematic.kinematic_equations_utils import variation, resultant
import pandas as pd
from kinematic.dataset_smoothing import smooth
from variables.constants import SECOND, X_POSITION_ABSOLUTE, Y_POSITION_ABSOLUTE, VISIBILITY

class JointKinematics:
    def __init__(self, joint_df: pd.DataFrame) -> None:
        """Models the kinematics datasets for a given joint"""
        self.t = joint_df[SECOND].to_numpy()
        self.x_position = joint_df[X_POSITION_ABSOLUTE].to_numpy()
        self.y_position = joint_df[Y_POSITION_ABSOLUTE].to_numpy()
        self.p = joint_df[VISIBILITY].to_numpy()

        self.x_velocity = None
        self.y_velocity = None
        self.velocity = None
        self.x_accel = None
        self.y_accel = None
        self.accel = None
        self.x_position_smooth = None
        self.y_position_smooth = None
        self.x_velocity_smooth = None
        self.y_velocity_smooth = None
        self.velocity_smooth = None
        self.x_accel_smooth = None
        self.y_accel_smooth = None
        self.accel_smooth = None

        self.init_velocity()
        self.init_accel()
        self.smooth_curves()

    def init_accel(self):
        self.x_accel = variation(self.t, self.x_velocity)
        self.y_accel = variation(self.t, self.y_velocity)
        self.accel = resultant(self.x_velocity, self.y_velocity)

    def init_velocity(self):
        self.x_velocity = variation(self.t, self.x_position)
        self.y_velocity = variation(self.t, self.y_position)
        self.velocity = resultant(self.x_velocity, self.y_velocity) # TODO: may create tuples (velocity, direction) to plot the vectors

    def smooth_curves(self):
        """Smooths the curves using Savitzky-Golay filter. ALL curves are first calculated using raw data, then smoothed"""
        self.x_position_smooth = smooth(self.x_position)
        self.y_position_smooth = smooth(self.y_position)

        self.x_velocity_smooth = smooth(self.x_velocity)
        self.y_velocity_smooth = smooth(self.y_velocity)
        self.velocity_smooth = smooth(self.velocity)

        self.x_accel_smooth = smooth(self.x_accel)
        self.y_accel_smooth = smooth(self.y_accel)
        self.accel_smooth = smooth(self.accel)
    
    def __str__(self) -> str:
        """like java toString(), but for debugging purposes only"""
        return f'vx = {self.x_velocity} \n ax = {self.x_accel}'