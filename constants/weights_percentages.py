from enum import Enum


class BodyWeightPercentage(Enum):
    """
    Enum class to represent the percentage of the body weight that each body part represents
    each tuple[float, float] represents the (male, female) mean percentages.
    """
    HAND = (0.0065, 0.0075)
    FOREARM = (0.0187, 0.0157)
    UPPER_ARM = (0.0325, 0.029)
    