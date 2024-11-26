import pandas as pd

from constants.df_columns_names import JOINT_ID
from constants.joints_ids_to_names import get_joint_name, Joint
from drawings.vectors import KinematicsVectors
from globals.video_metadata import VideoMetadata
from kinematic.joint_kinematics import JointKinematics
from kinematic.steps import StepsCalculator
from pendulum.energy import Energy
from pendulum.solid_bar_pendulum import SolidBarPendulum


class JointAnalysis:
    def __init__(self, video_metadata: VideoMetadata, joint_raw_data: pd.DataFrame, joint_name: str) -> None:
        self.kinematics_data = JointKinematics(joint_raw_data)
        self.kinematics_vectors = KinematicsVectors(self.kinematics_data, video_metadata)
        self.joint_name = joint_name


class VideoAnalysis:
    def __init__(self, video_metadata: VideoMetadata, joints_raw_data: pd.DataFrame) -> None:
        self.video_metadata = video_metadata
        self.joints_raw_data = joints_raw_data
        self.joints_analysis: dict[int, JointAnalysis] = {}
        self.pendulum = None
        self.energy_analysis = None
        self.steps = None
        self.analyse()

    def analyse(self):
        self.build_joints_data()
        self.build_pendulum_data()
        self.build_energy_data()
        self.build_steps()

    def build_joints_data(self):
        joints_raw_grouped = self.joints_raw_data.groupby(JOINT_ID)
        self.joints_analysis = {joint_id: JointAnalysis(self.video_metadata, joint_data, get_joint_name(joint_id)) for joint_id, joint_data in joints_raw_grouped}

    def build_pendulum_data(self):
        self.pendulum = SolidBarPendulum(
            self.joints_analysis[Joint.RIGHT_SHOULDER.value].kinematics_data,
            self.joints_analysis[Joint.RIGHT_ELBOW.value].kinematics_data,
            self.joints_analysis[Joint.RIGHT_WRIST.value].kinematics_data,
            self.video_metadata.subject_mass,
        )

    def build_energy_data(self):
        self.energy_analysis = Energy(self.pendulum)

    def build_steps(self):
        self.steps = StepsCalculator(self.joints_analysis[Joint.RIGHT_HEEL.value].kinematics_data.y_position_smooth).find_steps()
