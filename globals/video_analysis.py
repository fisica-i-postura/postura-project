import pandas as pd

from constants.df_columns_names import JOINT_ID
from drawings.vectors import KinematicsVectors
from globals.video_metadata import VideoMetadata
from kinematic.joint_kinematics import JointKinematics


class JointAnalysis:
    def __init__(self, video_metadata: VideoMetadata, joint_raw_data: pd.DataFrame) -> None:
        self.kinematics_data = JointKinematics(joint_raw_data)
        self.kinematics_vectors = KinematicsVectors(self.kinematics_data, video_metadata)


class VideoAnalysis:
    def __init__(self, video_metadata: VideoMetadata, joints_raw_data: pd.DataFrame) -> None:
        self.video_metadata = video_metadata
        self.joints_raw_data = joints_raw_data
        self.joints_analysis: dict[int, JointAnalysis] = {}
        self.analyse()

    def analyse(self):
        self.build_joints_data()
        """
        TODO: Implement the analysis of the video
            process videos to pandas
            build joints data
            build joints kinematics data
            build plots
            build drawings
        """
        pass

    def build_joints_data(self):
        joints_raw_grouped = self.joints_raw_data.groupby(JOINT_ID)
        self.joints_analysis = {joint_id: JointAnalysis(self.video_metadata, joint_data) for joint_id, joint_data in joints_raw_grouped}
