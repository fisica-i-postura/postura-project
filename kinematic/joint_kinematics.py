from kinematic_equiations_utils import variation, resultant
import pandas as pd

class JointKinematics:
    def __init__(self, joint_df: pd.DataFrame) -> None:
        """Models the kinematics datasets for a given joint"""
        self.t = joint_df['second'].to_numpy()
        self.x_position = joint_df['x_abs'].to_numpy()      
        self.y_position = joint_df['y_abs'].to_numpy()
        self.p = joint_df["v"].to_numpy()

        self.x_velocity = variation(self.t, self.x_position)
        self.y_velocity = variation(self.t, self.y_position)
        self.velocity = resultant(self.x_velocity, self.y_velocity)
        """TODO: may create tuples (velocity, direction) to plot the vectors"""

        self.x_accel = variation(self.t, self.x_velocity)
        self.y_accel = variation(self.t, self.y_velocity)
        self.accel = resultant(self.x_velocity, self.y_velocity)

    def __str__(self) -> str:
        """like java toString(), but for debugging purposes only"""
        return f'vx = {self.x_velocity} \n ax = {self.x_accel}'