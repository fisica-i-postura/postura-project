import cv2

from drawings.draw_helper import DrawHelper
from drawings.draw_configs import DrawAxis, DrawType, JointDrawConfig
from globals.video_analysis import VideoAnalysis
from drawings.colors import Color


def get_draw_configs() -> list[JointDrawConfig]:
    return [
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.RED.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.X, color=Color.RED.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.Y, color=Color.RED.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.R, color=Color.BLUE.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.X, color=Color.BLUE.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.Y, color=Color.BLUE.value),
    ]


def display(video_path: str, video_analysis: VideoAnalysis, joints_to_track: dict[int, str]|None) -> None:
    cap = cv2.VideoCapture(video_path)

    # Verificar si el video se pudo abrir
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
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()