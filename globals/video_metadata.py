from dataclasses import dataclass

@dataclass
class VideoMetadata:
    path: str
    fps: float
    resolution: tuple[int, int]
    subject_gender: str
    subject_mass: float
    pixels_per_meter: float
    baseline_offset_in_px: float