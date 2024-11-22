import logging
import os
from pathlib import Path

from globals.io.paths import get_videos_folder_path, PathHelper
from globals.physics_processor import PhysicsProcessor, UserInput
from globals.io.dataclasses import read_json_to_dataclass

videos_dir = get_videos_folder_path()


def get_videos_paths():
    files = os.listdir(videos_dir)
    return [os.path.join(videos_dir, file) for file in files]

def bulk_process_videos():
    for path in get_videos_paths():
        path_helper = PathHelper(Path(path))
        input_path = path_helper.get_user_input_path()
        if not input_path.exists():
            logging.log(logging.ERROR, f'User input for {path} not found, skipping...')
            continue
        user_input = read_json_to_dataclass(input_path, UserInput)
        user_input.video_path = path
        PhysicsProcessor(user_input)