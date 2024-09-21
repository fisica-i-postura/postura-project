import pandas as pd
from joint_kinematics import JointKinematics

class JointsToKinematicsData:
    def __init__(self, df: pd.DataFrame) -> None:
        joints = df.groupby('a')
        self._joint_id_to_kinematics_map = {joint_id: JointKinematics(data) for joint_id, data in joints}

    def get_joint(self, joint_id: int):
        return self._joint_id_to_kinematics_map[joint_id]
    
    def __str__(self) -> str:
        s = 'Joints Data: \n'
        for joint, kinematics in self._joint_id_to_kinematics_map.items():
            s += f'{joint} -> {kinematics.__str__()} \n'
        return s