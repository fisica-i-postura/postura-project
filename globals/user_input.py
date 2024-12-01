from dataclasses import dataclass
from enum import Enum


class Gender(Enum):
    MALE = 'M'
    FEMALE = 'F'


@dataclass
class UserInput:
    video_path: str
    shoulder_elbow_distance_in_meters: float = 0.33
    subject_gender: Gender = Gender.MALE
    subject_weight: float = 85.0
