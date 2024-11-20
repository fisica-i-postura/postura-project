from math import isnan

import cv2
import numpy as np

from drawings.vectors import Vector

Shape = Vector|None

def to_cv2_point(point: tuple[int, int], video_height) -> tuple[int, int]:
    x, y = point
    if isnan(x) or isnan(y):
        return 0, 0
    return int(x), int(video_height - y)


def draw_vector(frame: np.ndarray, vector: Vector, video_height):
    pt1 = to_cv2_point(vector.origin, video_height)
    pt2 = to_cv2_point(vector.translation, video_height)
    cv2.arrowedLine(frame, pt1, pt2, (0, 0, 255), 2)


def draw_shape(frame: np.ndarray, shape: Shape|list[Shape], video_height: int = 1080):
    if shape is None:
        return frame

    elif isinstance(shape, list):
        for s in shape:
            frame = draw_shape(frame, s, video_height)

    elif isinstance(shape, Vector):
        draw_vector(frame, shape, video_height)

    return frame