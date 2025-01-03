from dataclasses import dataclass
from math import isnan

import cv2
import numpy as np

from drawings.draw_configs import DrawAxis
from drawings.vectors import Vector

Point = tuple[int, int] | tuple[float, float]
DrawablePoint = tuple[int, int]
Color = tuple[int, int, int]

@dataclass
class Line:
    p1: Point
    p2: Point
    label: str = ""

Shape = Vector | Line | Point | None

TEXT_PADDING_PX = 25

class Cv2DrawUtils:

    def __init__(self, video_height: int) -> None:
        self.video_height = video_height

    def draw_shape(self, frame: np.ndarray, shape: Shape | list[Shape], color: Color, axis: DrawAxis|list[DrawAxis]) -> np.ndarray:
        if shape is None:
            return frame
        elif isinstance(shape, list):
            for s in shape:
                frame = self.draw_shape(frame, s, color, axis)
        elif isinstance(shape, Vector):
            self.draw_vector(frame, shape, color, axis)
        elif isinstance(shape, Line):
            self.draw_line(frame, shape, color)
        elif isinstance(shape, tuple) and all(isinstance(p, (int, float)) for p in shape):
            self.draw_line(frame, Line(shape, shape), color, 10)
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
        match axis:
            case DrawAxis.R:
                cv2.putText(frame, f'{vector.magnitude:.2f} m', (px + TEXT_PADDING_PX, py + TEXT_PADDING_PX), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.arrowedLine(frame, p0, point, color, 2)
            case DrawAxis.X:
                magnitude = abs((px - x0) / vector.pixels_per_meters)
                cv2.putText(frame, f'{magnitude :.2f} m', (px + TEXT_PADDING_PX, y0 + TEXT_PADDING_PX), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.arrowedLine(frame, p0, (px, y0), color, 2)
            case DrawAxis.Y:
                magnitude = abs((py - y0) / vector.pixels_per_meters)
                cv2.putText(frame, f'{magnitude :.2f} m', (x0 + TEXT_PADDING_PX, py + TEXT_PADDING_PX), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                cv2.arrowedLine(frame, p0, (x0, py), color, 2)

    def draw_line(self, frame: np.ndarray, line: Line, color: Color, thickness = 2) -> None:
        p1 = self.to_cv2_point(line.p1)
        p2 = self.to_cv2_point(line.p2)
        cv2.line(frame, p1, p2, color, thickness)
        if line.label:
            cv2.putText(frame, line.label, (p1[0] + TEXT_PADDING_PX, p1[1] + TEXT_PADDING_PX) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    def to_cv2_point(self, point: Point) -> DrawablePoint:
        x, y = point
        if isnan(x) or isnan(y):
            return 0, 0
        return int(x), int(self.video_height - y)

