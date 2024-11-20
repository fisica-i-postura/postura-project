import numpy as np

from drawings.cv2_draw_utils import Shape, Cv2DrawUtils
from drawings.draw_configs import DrawType, JointDrawConfig
from drawings.vectors import KinematicsVectors
from globals.video_analysis import VideoAnalysis


def get_shape(kinematic_vectors: KinematicsVectors, draw_type: DrawType, frame_idx: int) -> Shape:
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
            shape = get_shape(joint_analysis, joint_draw_config.draw_type, frame_idx)
            self.cv2_draw_util.draw_vector(frame, shape, joint_draw_config.color, joint_draw_config.draw_axis)