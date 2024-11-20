import numpy as np

from globals.video_metadata import VideoMetadata
from kinematic.joint_kinematics import JointKinematics

class Vector:
    def __init__(self, xy: tuple[int, int], origin: tuple[int, int] = (0, 0), magnitude: float = -1) -> None:
        self.xy = xy
        self.origin = origin
        self.translation = (origin[0] + xy[0], origin[1] + xy[1])
        self.magnitude = magnitude if magnitude >= 0 else self.calculate_magnitude()

    def calculate_magnitude(self):
        x, y = self.xy
        return (x**2 + y**2)**0.5


class KinematicsVectors:

    def __init__(self, kinematics_data: JointKinematics, video_metadata: VideoMetadata) -> None:
        self.kinematics_data = kinematics_data
        self.video_metadata = video_metadata
        self.position_vectors = self.build_position_vectors()
        self.velocity_vectors = self.build_velocity_vectors()
        self.acceleration_vectors = self.build_acceleration_vectors()

    def build_position_vectors(self):
        x_pos_in_px = self.kinematics_data.x_position
        y_pos_in_px = self.kinematics_data.y_position
        o_vector = Vector((0, 0))
        origins = [o_vector] * len(x_pos_in_px)
        return self.build_vectors((x_pos_in_px, y_pos_in_px), origins, self.kinematics_data.position)

    def build_velocity_vectors(self):
        return self.build_vectors((self.kinematics_data.x_velocity, self.kinematics_data.y_velocity), self.position_vectors, self.kinematics_data.velocity)

    def build_acceleration_vectors(self):
        return self.build_vectors((self.kinematics_data.x_accel, self.kinematics_data.y_accel), self.position_vectors, self.kinematics_data.accel)

    def build_vectors(self, xys: (np.ndarray[float], np.ndarray[float]), origins: list[Vector], magnitudes: np.ndarray[float]):
        x, y = xys
        x_in_px = x * self.video_metadata.pixels_per_meter
        y_in_px = y * self.video_metadata.pixels_per_meter
        magnitude_in_px = magnitudes * self.video_metadata.pixels_per_meter
        return [Vector((x, y), o.translation, m) for x, y, o, m in zip(x_in_px, y_in_px, origins, magnitude_in_px)]