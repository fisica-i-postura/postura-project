import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pandas as pd

from globals.io.dataclasses import read_json_to_dataclass, write_dataclass_to_json
from globals.io.paths import PathHelper, get_csv_folder_path
from globals.video_analysis import VideoAnalysis
from globals.video_metadata import VideoMetadata
from pendulum.model import Pendulum
from pendulum.plot import plot_pendulum
from plotting.kinematics_plots import KinematicsPlotHelper
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
        self.path_helper = PathHelper(Path(user_input.video_path))
        self.video_metadata, self.video_raw_data = self._find_data_or_process()
        self.video_analysis = VideoAnalysis(self.video_metadata, self.video_raw_data)
        self._create_plots_if_needed()

    def _find_data_or_process(self) -> tuple[VideoMetadata, pd.DataFrame]:
        metadata_path = self.path_helper.get_metadata_path()
        csv_path = self.path_helper.get_csv_path()

        if metadata_path.exists() and csv_path.exists():
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

    def _create_plots_if_needed(self):
        directory = self.path_helper.get_plots_folder_path()
        if directory.exists() and directory.is_dir():
            for file in directory.iterdir():
                if file.is_file():
                    file.unlink()

        for joint_id, analysis in self.video_analysis.joints_analysis.items():
            KinematicsPlotHelper(analysis.kinematics_data, analysis.joint_name, directory, self.video_analysis.steps).plot()

        process_pendulum()


def process_pendulum():
    for path in get_csv_paths():
        pendulum = Pendulum(pd.read_csv(path))
        plot_pendulum(pendulum, 'resources/plots/' + os.path.basename(path).split(".")[0] + '/pendulum.png')


csv_dir = get_csv_folder_path()


def get_csv_paths():
    files = os.listdir(csv_dir)
    return [os.path.join(csv_dir, file) for file in files]
