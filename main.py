import os

import cv2
import pandas as pd

from constants.joints_ids_to_names import joints_to_track
from globals.video_analysis import VideoAnalysis
from globals.video_display import display
from globals.video_metadata import VideoMetadata
from kinematic.joints_to_kinematics_data import JointsToKinematicsData
from pendulum.model import Pendulum
from pendulum.plot import plot_pendulum
from plotting.graphics_visualization import plot_joint_kinematics
from tracking.tracker import VideoInput, VideoTracker

videos_dir = './resources/videos'
def get_videos_paths():
    files = os.listdir(videos_dir)
    return [os.path.join(videos_dir, file) for file in files]


def get_csv_path(path: str):
    return path.replace('.mov', '.csv').replace('videos', 'csv')


def process_videos(paths: list[str]):
    for path in paths:
        video_input = VideoInput(path, 12, 14, 0.33)
        video_output = VideoTracker(video_input).process()
        video_output.dataframe.to_csv(get_csv_path(path))

csv_dir = './resources/csv'
def get_csv_paths():
    files = os.listdir(csv_dir)
    return [os.path.join(csv_dir, file) for file in files]


def build_kinematics_data() -> list[JointsToKinematicsData]:
    paths = get_csv_paths()
    return [JointsToKinematicsData(pd.read_csv(path), 'resources/plots/' + os.path.basename(path).split(".")[0]) for path in paths]


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


# if __name__ == '__main__':
#     videos_paths = get_videos_paths()
#     process_videos(videos_paths)
#     kinematics_data = build_kinematics_data()
#     process_kinematics_plots(kinematics_data)
#     process_pendulum()
#     print('Proceso finalizado')

if __name__ == '__main__':
    for video in get_videos_paths():
        cap = cv2.VideoCapture(video)
        df = pd.read_csv(get_csv_path(video))
        metadata = VideoMetadata((1920, 1080), 1/0.0019805559026734917)
        analysis = VideoAnalysis(metadata, df)
        display(video, analysis, None)