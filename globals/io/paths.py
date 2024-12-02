from pathlib import Path

ROOT = '../postura-project'
RESOURCES = f'{ROOT}/resources'
USER_INPUTS = f'{RESOURCES}/user_inputs'
VIDEOS = f'{RESOURCES}/videos'
CSV = f'{RESOURCES}/csv'
PLOTS = f'{RESOURCES}/plots'
METADATA = f'{RESOURCES}/metadata'
PROCESSED = f'{RESOURCES}/processed'


def get_folder(name, create):
    folder = Path(f'{name}')
    if create and not folder.exists():
        folder.mkdir()
    return folder


def get_user_inputs_folder_path(create: bool = True) -> Path:
    return get_folder(USER_INPUTS, create)


def get_videos_folder_path(create: bool = True) -> Path:
    return get_folder(VIDEOS, create)


def get_csv_folder_path(create: bool = True) -> Path:
    return get_folder(CSV, create)


def get_metadata_folder_path(create: bool = True) -> Path:
    return get_folder(METADATA, create)

def get_processed_folder_path(create: bool = True) -> Path:
    return get_folder(PROCESSED, create)


class PathHelper:
    def __init__(self, path: Path):
        self.path = path
        self.stem = path.stem
        self.suffix = path.suffix

    def get_user_input_path(self) -> Path:
        return Path(f'{get_user_inputs_folder_path()}/{self.stem}.json')

    def get_csv_path(self) -> Path:
        return Path(f'{get_csv_folder_path()}/{self.stem}.csv')

    def get_plots_folder_path(self, create: bool = True) -> Path:
        folder = Path(f'{PLOTS}/{self.stem}')
        if create and not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        return folder

    def get_metadata_path(self) -> Path:
        return Path(f'{get_metadata_folder_path()}/{self.stem}.json')

    def get_processed_video_folder(self) -> Path:
        folder = Path(f'{get_processed_folder_path()}/{self.stem}_processed')
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        return folder

    def get_processed_video_path(self) -> Path:
        return Path(f'{self.get_processed_video_folder()}/{self.stem}_processed.mp4')