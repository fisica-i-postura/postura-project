from pathlib import Path

import cv2

from constants.joints_ids_to_names import Joint
from drawings.draw_helper import DrawHelper
from drawings.draw_configs import DrawAxis, DrawType, JointDrawConfig
from globals.io.paths import PathHelper
from globals.video_analysis import VideoAnalysis
from drawings.colors import Color


def get_draw_configs() -> list[JointDrawConfig]:
    return [
        JointDrawConfig(joint_id=Joint.RIGHT_SHOULDER.value, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.GREEN.value, trace=True),
        JointDrawConfig(joint_id=Joint.RIGHT_WRIST.value, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.YELLOW.value, trace=True),
        JointDrawConfig(joint_id=Joint.RIGHT_ELBOW.value, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.RED.value, trace=True),
        JointDrawConfig(joint_id=Joint.RIGHT_ELBOW.value, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.R, color=Color.BLUE.value),
        JointDrawConfig(joint_id=Joint.RIGHT_ELBOW.value, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.X, color=Color.BLUE.value),
        JointDrawConfig(joint_id=Joint.RIGHT_ELBOW.value, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.Y, color=Color.BLUE.value),
        JointDrawConfig(joint_id=Joint.RIGHT_HEEL.value, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.ORANGE.value, trace=True),
        JointDrawConfig(joint_id=Joint.RIGHT_HEEL.value, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.R, color=Color.CYAN.value),
        JointDrawConfig(joint_id=Joint.RIGHT_HEEL.value, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.X, color=Color.CYAN.value),
        JointDrawConfig(joint_id=Joint.RIGHT_HEEL.value, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.Y, color=Color.CYAN.value),
        JointDrawConfig(joint_id=Joint.RIGHT_ELBOW.value, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.MAGENTA.value, trace=True),
        JointDrawConfig(joint_id=Joint.RIGHT_WRIST.value, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.TEAL.value, trace=True),
    ]


def display(video_path: str, video_analysis: VideoAnalysis) -> None:
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Initialize VideoWriter
    out_path = PathHelper(Path(video_path)).get_processed_video_path().__str__()
    out = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height))

    if not cap.isOpened():
        print("Error: No se pudo abrir el video.")
        exit()

    draw_helper = DrawHelper(video_analysis, get_draw_configs())

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        draw_helper.draw(frame, frame_idx)
        # draw_helper.draw_pendulum_angle(frame, frame_idx)
        out.write(frame)
        # cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_idx += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()