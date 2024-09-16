import pandas as pd
from joint_kinematics import JointKinematics

"""TODO: extract to main file when integrating changes"""
PATH = './joints_per_second.csv'
df = pd.read_csv(PATH)

class JointsToKinematicsData:
    def __init__(self, df: pd.DataFrame) -> None:
        self._joint_id_to_kinematics_map = {}
        joints = df.groupby('a')
        for joint_id, data in joints:
            self._joint_id_to_kinematics_map[joint_id] = JointKinematics(data)

    def get_joint(self, id: int):
        return self._joint_id_to_kinematics_map[id]
    
    def __str__(self) -> str:
        s = 'Joints Data: \n'
        for joint, kinematics in self._joint_id_to_kinematics_map.items():
            s += f'{joint} -> {kinematics.__str__()} \n'
        return s

print(JointsToKinematicsData(df).__str__())