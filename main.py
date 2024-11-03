import os
from pendulum.plot import plot_pendulum
from tracking.track_joints_to_pandas_csv import video_to_csv
import pandas as pd
from kinematic.joints_to_kinematics_data import JointsToKinematicsData
from constants.joints_ids_to_names import joints_to_track
from plotting.graphics_visualization import plot_joint_kinematics
from pendulum.model import Pendulum

videos_dir = './resources/videos'
def get_videos_paths():
    files = os.listdir(videos_dir)
    return [os.path.join(videos_dir, file) for file in files]


def get_csv_path(path: str):
    return path.replace('.mp4', '.csv').replace('videos', 'csv')


def process_videos(paths: list[str]):
    for path in paths:
        csv_path = get_csv_path(path)
        output_video_path = path.replace('.mp4', '_processed.mp4').replace('videos', './resources/processed_videos')
        video_to_csv(path, csv_path, output_video_path)



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


if __name__ == '__main__':
    videos_paths = get_videos_paths()
    process_videos(videos_paths)
    kinematics_data = build_kinematics_data()
    process_kinematics_plots(kinematics_data)
    process_pendulum()
    print('Proceso finalizado')