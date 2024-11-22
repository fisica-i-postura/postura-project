import os

from globals.io.paths import get_videos_folder_path

videos_dir = get_videos_folder_path()


def get_videos_paths():
    files = os.listdir(videos_dir)
    return [os.path.join(videos_dir, file) for file in files]
