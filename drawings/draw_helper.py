from dataclasses import dataclass

import numpy as np

from drawings.cv2_draw_utils import Shape, Cv2DrawUtils
from drawings.vectors import KinematicsVectors
from globals.video_analysis import VideoAnalysis
from enum import Enum, auto


Color = tuple[int, int, int]


class DrawAxis(Enum):
    X = auto()
    Y = auto()
    R = auto()


class DrawType(Enum):
    POSITION = auto()
    VELOCITY = auto()
    ACCELERATION = auto()


@dataclass
class JointDrawConfig:
    joint_id: int
    draw_type: DrawType
    draw_axis: DrawAxis
    color: Color


def get_shapes(kinematic_vectors: KinematicsVectors, draw_type: DrawType, frame_idx: int) -> list[Shape]:
    match draw_type:
        case DrawType.POSITION:
            return kinematic_vectors.position_vectors[frame_idx]
        case DrawType.VELOCITY:
            return kinematic_vectors.velocity_vectors[frame_idx]
        case DrawType.ACCELERATION:
            return kinematic_vectors.acceleration_vectors[frame_idx]


class DrawHelper:
    def __init__(self, video_analysis: VideoAnalysis, joint_draw_configs: list[JointDrawConfig]) -> None:
        self.joints_analysis = video_analysis.joints_analysis
        self.joint_draw_configs = joint_draw_configs
        self.cv2_draw_util = Cv2DrawUtils(video_analysis.video_metadata.resolution[1])

    def draw(self, frame: np.ndarray, frame_idx: int):
        for joint_draw_config in self.joint_draw_configs:
            joint_analysis = self.joints_analysis[joint_draw_config.joint_id].kinematics_vectors
            vectors = get_shapes(joint_analysis, joint_draw_config.draw_type, frame_idx)
            self.draw_shapes(frame, vectors, joint_draw_config)

    def draw_shapes(self, frame, vectors, joint_draw_config):
        for vector in vectors:
            self.cv2_draw_util.draw_vector(frame, vector, joint_draw_config.color)
