from dataclasses import dataclass
from enum import Enum, auto

from drawings.colors import Color


class DrawAxis(Enum):
    X = auto()
    Y = auto()
    R = auto()


class DrawType(Enum):
    POSITION = auto()
    VELOCITY = auto()
    ACCELERATION = auto()


@dataclass
class JointDrawConfig:
    joint_id: int
    draw_type: DrawType
    draw_axis: DrawAxis
    color: Color
