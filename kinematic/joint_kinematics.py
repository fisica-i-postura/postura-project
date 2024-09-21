from kinematic_equations_utils import variation, resultant
import pandas as pd
from dataset_smoothing import smooth

class JointKinematics:
    def __init__(self, joint_df: pd.DataFrame) -> None:
        """Models the kinematics datasets for a given joint"""
        self.t = joint_df['second'].to_numpy()
        self.x_position = joint_df['x_abs'].to_numpy()
        self.y_position = joint_df['y_abs'].to_numpy()
        self.p = joint_df["v"].to_numpy()

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
        self.x_accel_smooth = None
        self.y_accel_smooth = None

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
        self.x_position_smooth = smooth(self.x_position)
        self.y_position_smooth = smooth(self.y_position)

        self.x_velocity_smooth = variation(self.t, self.x_position_smooth)
        self.y_velocity_smooth = variation(self.t, self.y_position_smooth)

        self.x_accel_smooth = variation(self.t, self.x_velocity_smooth)
        self.y_accel_smooth = variation(self.t, self.y_velocity_smooth)
    
    def __str__(self) -> str:
        """like java toString(), but for debugging purposes only"""
        return f'vx = {self.x_velocity} \n ax = {self.x_accel}'