from kinematic_equations import velocity, acceleration
import numpy as np
import pandas as pd

def resultant(x, y):
    return np.sqrt(np.square(x) + np.square(y))

def direction(x, y):
    return np.arctan(x, y)

class JointKinematics:
    def __init__(self, joint_df: pd.DataFrame) -> None:
        self.t = joint_df['second'].to_numpy()
        self.x_position = joint_df['x_abs'].to_numpy()      
        self.y_position = joint_df['y_abs'].to_numpy()
        self.p = joint_df["v"].to_numpy()

        self.x_velocity = velocity(self.t, self.x_position)
        self.y_velocity = velocity(self.t, self.y_position)
        self.velocity = resultant(self.x_velocity, self.y_velocity)

        self.x_accel = acceleration(self.t, self.x_velocity)
        self.y_accel = acceleration(self.t, self.y_velocity)
        self.accel = resultant(self.x_velocity, self.y_velocity)

    def __str__(self) -> str:
        return f't = {self.t}'