from kinematic.kinematic_equations_utils import variation, resultant
import pandas as pd
from kinematic.dataset_smoothing import smooth
from constants.df_columns_names import SECOND, X_POSITION_ABSOLUTE, Y_POSITION_ABSOLUTE, VISIBILITY

class JointKinematics:
    def __init__(self, joint_df: pd.DataFrame, name: str = "unknown") -> None:
        """Models the kinematics datasets for a given joint"""
        self.name = name
        self.t = joint_df[SECOND].to_numpy()
        self.x_position = joint_df[X_POSITION_ABSOLUTE].to_numpy()
        self.y_position = joint_df[Y_POSITION_ABSOLUTE].to_numpy()
        self.p = joint_df[VISIBILITY].to_numpy()

        self.x_position_smooth = smooth(self.x_position)
        self.y_position_smooth = smooth(self.y_position)
        self.position = resultant(self.x_position, self.y_position)

        self.x_velocity = self.x_velocity_smooth = variation(self.t, self.x_position_smooth)
        self.y_velocity = self.y_velocity_smooth = variation(self.t, self.y_position_smooth)
        self.velocity = self.velocity_smooth = resultant(self.x_velocity, self.y_velocity)
        self.x_accel = self.x_accel_smooth = variation(self.t, self.x_velocity)
        self.y_accel = self.y_accel_smooth = variation(self.t, self.y_velocity)
        self.accel = self.accel_smooth = resultant(self.x_accel, self.y_accel)
    
    def __str__(self) -> str:
        """like java toString(), but for debugging purposes only"""
        return f'vx = {self.x_velocity} \n ax = {self.x_accel}'