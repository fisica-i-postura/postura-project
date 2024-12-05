from dataclasses import dataclass

import cv2
import mediapipe as mp
import pandas as pd
from constants.joints_ids_to_names import joints_to_track, Joint
from constants.df_columns_names import FRAME_INDEX, JOINT_ID, X_POSITION_NORMALIZED, Y_POSITION_NORMALIZED, VISIBILITY, \
    X_POSITION_ABSOLUTE, Y_POSITION_ABSOLUTE, SECOND, X_POSITION_IN_PX, Y_POSITION_IN_PX


@dataclass
class VideoInput:
    path: str
    src_joint: int
    dst_joint: int
    joints_distance_in_meters: float


@dataclass
class VideoOutput:
    dataframe: pd.DataFrame
    resolution: tuple[int, int]
    fps: float
    pixels_per_meter: float
    base_line_offset_in_px: float = 0


class VideoTracker:
    def __init__(self, video_input: VideoInput):
        self.video_input = video_input
        self.df: pd.DataFrame | None = None
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            min_tracking_confidence=0.5
        )
        self.resolution: tuple[int, int] | None = None
        self.fps: float | None = None
        self.pixels_per_meter: float | None = None
        self.baseline_offset_in_px: float | None = None

    def process(self) -> VideoOutput:
        self._process_video()
        self._adjust_data()
        return VideoOutput(self.df, self.resolution, self.fps, self.pixels_per_meter, self.baseline_offset_in_px)

    def _process_video(self):
        cap = cv2.VideoCapture(self.video_input.path)

        if not cap.isOpened():
            raise Exception(f"Failed to open video: {self.video_input.path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.resolution = (width, height)
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        data = []
        frame_number = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                for joint_id in joints_to_track:
                    joint = results.pose_landmarks.landmark[joint_id]

                    data.append({
                        FRAME_INDEX: frame_number,
                        JOINT_ID: joint_id,
                        X_POSITION_NORMALIZED: joint.x,
                        Y_POSITION_NORMALIZED: 1 - joint.y,
                        VISIBILITY: joint.visibility
                    })

            frame_number += 1

        cap.release()
        self.df = pd.DataFrame(data)

    def _adjust_data(self):
        self._denormalize_positions()
        self._adjust_height_to_heel_base()
        self._calculate_positions_in_meters()
        self._calculate_second_per_frame()

    def _denormalize_positions(self):
        self.df[X_POSITION_IN_PX] = self.df[X_POSITION_NORMALIZED] * self.resolution[0]
        self.df[Y_POSITION_IN_PX] = self.df[Y_POSITION_NORMALIZED] * self.resolution[1]

    def _adjust_height_to_heel_base(self):
        self.baseline_offset_in_px = min(self.df[self.df[JOINT_ID] == Joint.RIGHT_HEEL.value][Y_POSITION_IN_PX])
        self.df[Y_POSITION_IN_PX] = self.df[Y_POSITION_IN_PX] - self.baseline_offset_in_px

    def _calculate_positions_in_meters(self):
        conversion_factor = self.calculate_conversion_factor()
        self.df[X_POSITION_ABSOLUTE] = self.df[X_POSITION_IN_PX] * conversion_factor
        self.df[Y_POSITION_ABSOLUTE] = self.df[Y_POSITION_IN_PX] * conversion_factor

    def calculate_conversion_factor(self):
        joints_distance_in_px = self.calculate_pixel_distance()
        meters_pixel_distance = self.video_input.joints_distance_in_meters / joints_distance_in_px
        self.pixels_per_meter = 1 / meters_pixel_distance
        return meters_pixel_distance

    def calculate_pixel_distance(self):
        x_a, x_b, y_a, y_b = self._get_reference_joints_positions_in_px()
        pixel_distance = ((x_b - x_a) ** 2 + (y_b - y_a) ** 2) ** 0.5
        return pixel_distance

    def _get_reference_joints_positions_in_px(self):
        dst_joint_data, src_joint_data = self._get_reference_joints_data()
        x_a = src_joint_data.iloc[0][X_POSITION_IN_PX]
        y_a = src_joint_data.iloc[0][Y_POSITION_IN_PX]
        x_b = dst_joint_data.iloc[0][X_POSITION_IN_PX]
        y_b = dst_joint_data.iloc[0][Y_POSITION_IN_PX]
        return x_a, x_b, y_a, y_b

    def _get_reference_joints_data(self):
        src_joint_data = self.df[self.df[JOINT_ID] == self.video_input.src_joint]
        dst_joint_data = self.df[self.df[JOINT_ID] == self.video_input.dst_joint]
        return dst_joint_data, src_joint_data

    def _calculate_second_per_frame(self):
        self.df[SECOND] = self.df[FRAME_INDEX] / self.fps
