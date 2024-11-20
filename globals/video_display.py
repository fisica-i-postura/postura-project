import cv2

from drawings.draw_helper import DrawHelper, JointDrawConfig, DrawType, DrawAxis
from globals.video_analysis import VideoAnalysis


def get_draw_configs() -> list[JointDrawConfig]:
    return [
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=(0, 0, 255)),
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

        cv2.line(frame, (0, 0), (100, 100), (255, 0, 0), 5)
        # draw_shape(frame, video_analysis.joints_analysis[12].kinematics_vectors.position_vectors[frame_idx])
        # draw_shape(frame, video_analysis.joints_analysis[12].kinematics_vectors.velocity_vectors[frame_idx])
        # draw_shape(frame, video_analysis.joints_analysis[12].kinematics_vectors.acceleration_vectors[frame_idx])
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()