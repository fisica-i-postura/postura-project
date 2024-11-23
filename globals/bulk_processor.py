import logging
import os
from pathlib import Path

from globals.io.paths import get_videos_folder_path, PathHelper
from globals.physics_processor import PhysicsProcessor, UserInput, Gender
from globals.io.dataclasses import read_json_to_dataclass
from plotting.kinematics_plots import KinematicsPlotHelper

videos_dir = get_videos_folder_path()


def get_videos_paths():
    files = os.listdir(videos_dir)
    return [os.path.join(videos_dir, file) for file in files]

def bulk_process_videos():
    for path in get_videos_paths():
        path_helper = PathHelper(Path(path))
        input_path = path_helper.get_user_input_path()
        if not input_path.exists():
            logging.log(logging.WARN, f'User input for {path} not found, skipping...')
            continue
        user_input = get_user_input(input_path, path)
        p = PhysicsProcessor(user_input)
        jas = p.video_analysis.joints_analysis
        for joint_id, ja in jas.items():
            KinematicsPlotHelper(ja.kinematics_data, ja.joint_name, path_helper.get_plots_folder_path()).plot()
            pass


def get_user_input(input_path, path):
    user_input: UserInput = read_json_to_dataclass(input_path, UserInput)
    user_input.video_path = path
    if isinstance(user_input.subject_gender, str):
        user_input.subject_gender = Gender(user_input.subject_gender)
    return user_input