import numpy as np

from globals.video_analysis import VideoAnalysis
from enum import Enum, auto

class DrawAxis(Enum):
    X = auto()
    Y = auto()
    R = auto()


class DrawType(Enum):
    POSITION = auto()
    VELOCITY = auto()
    ACCELERATION = auto()


class DrawHelper:
    def __init__(self, video_analysis: VideoAnalysis) -> None:
        self.video_analysis = video_analysis

    def draw(self, frame: np.ndarray, frame_idx: int, joints: list[int], draw_type: DrawType, draw_axis: DrawAxis):
        for joint_id in joints:
            joint_analysis = self.video_analysis.joints_analysis[joint_id]
            vectors = getattr(joint_analysis.kinematics_vectors, f'{draw_type.name.lower()}_vectors')
            for vector in vectors:
                self.draw_vector(frame, vector, draw_axis)