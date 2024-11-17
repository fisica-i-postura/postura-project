import cv2
import numpy as np

from drawings.vectors import Vector

Shape = Vector|None

def to_cv2_point(point: tuple[int, int], video_height):
    x, y = point
    return x, video_height - y


def draw_vector(frame: np.ndarray, vector: Vector, video_height):
    cv2.arrowedLine(frame, to_cv2_point(vector.origin, video_height), to_cv2_point(vector.translation, video_height), (0, 0, 255), 2)


def draw_shape(frame: np.ndarray, shape: Shape|list[Shape], video_height: int = 1080):
    if shape is None:
        return frame

    elif isinstance(shape, list):
        for s in shape:
            frame = draw_shape(frame, s, video_height)

    elif isinstance(shape, Vector):
        draw_vector(frame, shape, video_height)

    return frame