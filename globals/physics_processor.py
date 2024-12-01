from pathlib import Path

import pandas as pd

from globals.io.dataclasses import read_json_to_dataclass, write_dataclass_to_json
from globals.io.paths import PathHelper
from globals.user_input import UserInput
from globals.video_analysis import VideoAnalysis
from globals.video_metadata import VideoMetadata
from plotting.energy_plots import EnergyPlotHelper
from plotting.kinematics_plots import KinematicsPlotHelper
from plotting.pendulum_plots import PendulumPlotHelper
from tracking.tracker import VideoInput, VideoTracker


def empty_dir(directory):
    if directory.exists() and directory.is_dir():
        for file in directory.iterdir():
            if file.is_file():
                file.unlink()


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
        video_metadata = VideoMetadata(video_input.path, video_output.fps, video_output.resolution, self.user_input.subject_gender.value, self.user_input.subject_weight, video_output.pixels_per_meter, video_output.base_line_offset_in_px)
        return video_metadata, video_output.dataframe

    def _create_plots_if_needed(self):
        directory = self.path_helper.get_plots_folder_path()
        empty_dir(directory)

        self.plot_kinematics(directory)
        self.plot_pendulum_angle(directory)
        self.plot_energy(directory)


    def plot_kinematics(self, directory):
        for joint_id, analysis in self.video_analysis.joints_analysis.items():
            KinematicsPlotHelper(analysis.kinematics_data, analysis.joint_name, directory,
                                 self.video_analysis.steps).plot()

    def plot_pendulum_angle(self, directory):
        PendulumPlotHelper(self.video_analysis.pendulum, self.video_analysis.steps, directory).plot()

    def plot_energy(self, directory):
        energy_data = self.video_analysis.energy_analysis
        EnergyPlotHelper(energy_data, self.video_analysis.steps, directory).plot()