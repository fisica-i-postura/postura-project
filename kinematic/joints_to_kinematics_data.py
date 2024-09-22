import pandas as pd
from kinematic.joint_kinematics import JointKinematics
from variables.constants import JOINT_ID

class JointsToKinematicsData:
    def __init__(self, df: pd.DataFrame, name) -> None:
        """Given a dataframe with joints data, models a map of joint_id to JointKinematics"""
        self.name = name
        joints = df.groupby(JOINT_ID)
        self._joint_id_to_kinematics_map = {joint_id: JointKinematics(data) for joint_id, data in joints}

    def get_joint(self, joint_id: int):
        return self._joint_id_to_kinematics_map[joint_id]
    
    def __str__(self) -> str:
        s = f'Joints Data for {self.name}: \n'
        for joint, kinematics in self._joint_id_to_kinematics_map.items():
            s += f'{joint} -> {kinematics.__str__()} \n'
        return s