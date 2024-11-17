from dataclasses import dataclass

@dataclass
class VideoMetadata:
    path: str
    fps: float
    duration: float
    resolution: tuple[int, int]
    subject_gender: str
    subject_length: float
    subject_mass: float
    pixels_per_meter: float