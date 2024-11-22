import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pandas as pd

from constants.joints_ids_to_names import joints_to_track
from globals.io.dataclasses import read_json_to_dataclass, write_dataclass_to_json
from globals.io.paths import PathHelper, get_csv_folder_path
from globals.video_analysis import VideoAnalysis
from globals.video_metadata import VideoMetadata
from kinematic.joints_to_kinematics_data import JointsToKinematicsData
from pendulum.model import Pendulum
from pendulum.plot import plot_pendulum
from plotting.graphics_visualization import plot_joint_kinematics
from tracking.tracker import VideoInput, VideoTracker


class Gender(Enum):
    MALE = 'M'
    FEMALE = 'F'


@dataclass
class UserInput:
    video_path: str
    joints_distance_in_meters: float = 0.33
    subject_gender: Gender = Gender.MALE
    subject_weight: float = 85.0


class PhysicsProcessor:
    def __init__(self, user_input: UserInput):
        self.user_input = user_input
        self.video_metadata, self.video_raw_data = self._find_data_or_process()
        self._create_plots_if_needed()
        self.video_analysis = VideoAnalysis(self.video_metadata, self.video_raw_data)

    def _find_data_or_process(self) -> tuple[VideoMetadata, pd.DataFrame]:
        path_helper = PathHelper(Path(self.user_input.video_path))
        metadata_path = path_helper.get_metadata_path()
        csv_path = path_helper.get_csv_path()

        if os.path.exists(metadata_path) and os.path.exists(csv_path):
            return read_json_to_dataclass(metadata_path, VideoMetadata), pd.read_csv(csv_path)
        else:
            video_metadata, video_data = self._process_video()
            write_dataclass_to_json(metadata_path, video_metadata)
            video_data.to_csv(csv_path)
            return video_metadata, video_data

    def _process_video(self) -> tuple[VideoMetadata, pd.DataFrame]:
        video_input = VideoInput(self.user_input.video_path, 12, 14, self.user_input.joints_distance_in_meters)
        video_output = VideoTracker(video_input).process()
        video_metadata = VideoMetadata(video_input.path, video_output.fps, video_output.resolution, self.user_input.subject_gender.value, self.user_input.subject_weight, video_output.pixels_per_meter)
        return video_metadata, video_output.dataframe

    @staticmethod
    def _create_plots_if_needed():
        process_kinematics_plots(build_kinematics_data())
        process_pendulum()


def build_kinematics_data() -> list[JointsToKinematicsData]:
    paths = get_csv_paths()
    return [JointsToKinematicsData(pd.read_csv(path), PathHelper(Path(path)).get_plots_folder_path().absolute()) for path in paths]


def process_kinematics_plots(joints_kinematics_data: list[JointsToKinematicsData]):
    for joints_kinematics in joints_kinematics_data:
        joint_ids = joints_to_track.keys()
        for joint_id in joint_ids:
            kinematics = joints_kinematics.get_joint(joint_id)
            plot_joint_kinematics(joint_id, kinematics, joints_kinematics.name)


def process_pendulum():
    for path in get_csv_paths():
        pendulum = Pendulum(pd.read_csv(path))
        plot_pendulum(pendulum, 'resources/plots/' + os.path.basename(path).split(".")[0] + '/pendulum.png')


csv_dir = get_csv_folder_path()


def get_csv_paths():
    files = os.listdir(csv_dir)
    return [os.path.join(csv_dir, file) for file in files]
