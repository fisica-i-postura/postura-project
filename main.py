from pathlib import Path

from globals.bulk_processor import bulk_process_videos
from globals.io.dataclasses import read_json_to_dataclass
from globals.io.paths import PathHelper, get_videos_folder_path
from globals.physics_processor import PhysicsProcessor, UserInput
from globals.video_display import display

# if __name__ == '__main__':
#     bulk_process_videos()

if __name__ == '__main__':
    path = get_videos_folder_path()
    for video in path.iterdir():
        path_helper = PathHelper(Path(video))
        user_input_file = path_helper.get_user_input_path()
        if not user_input_file.exists():
            continue
        user_input = read_json_to_dataclass(user_input_file, UserInput)
        user_input.video_path = video
        physics = PhysicsProcessor(user_input)
        display(video, physics.video_analysis)