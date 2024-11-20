from math import isnan

import cv2
import numpy as np

from drawings.draw_helper import Color, DrawAxis
from drawings.vectors import Vector

Shape = Vector | None
Point = tuple[int, int] | tuple[float, float]
DrawablePoint = tuple[int, int]


class Cv2DrawUtils:

    def __init__(self, video_height: int) -> None:
        self.video_height = video_height

    def draw_shape(self, frame: np.ndarray, shape: Shape | list[Shape], color: Color) -> np.ndarray:
        if shape is None:
            return frame
        elif isinstance(shape, list):
            for s in shape:
                frame = self.draw_shape(frame, s, color)
        elif isinstance(shape, Vector):
            self.draw_vector(frame, shape, color)
        return frame

    def draw_vector(self, frame: np.ndarray, vector: Vector, color: Color, axis: DrawAxis|list[DrawAxis]) -> None:
        if isinstance(axis, list):
            for a in axis:
                self.draw_vector(frame, vector, color, a)

        p0 = self.to_cv2_point(vector.origin)
        x0, y0 = p0
        point = self.to_cv2_point(vector.translation)
        px, py = point

        assert isinstance(axis, DrawAxis)
        match DrawAxis:
            case DrawAxis.R:
                cv2.putText(frame, f'{vector.magnitude:.2f} m', point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.arrowedLine(frame, p0, point, color, 2)
            case DrawAxis.X:
                cv2.arrowedLine(frame, p0, (px, y0), (0, 255, 0), 2)
            case DrawAxis.Y:
                cv2.arrowedLine(frame, p0, (x0, py), (255, 0, 0), 2)

    def to_cv2_point(self, point: Point) -> DrawablePoint:
        x, y = point
        if isnan(x) or isnan(y):
            return 0, 0
        return int(x), int(self.video_height - y)
