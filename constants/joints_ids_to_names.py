from enum import Enum

import mediapipe as mp

# Mapping of joint ids to joint names
l = mp.solutions.pose.PoseLandmark

def get_joint_name(joint_id: int) -> str:
    return mp.solutions.pose.PoseLandmark(joint_id).name.lower().replace("_", " ").capitalize()

class Joint(Enum):
    # RIGHT_EAR = 8
    RIGHT_WRIST = 16
    RIGHT_ELBOW = 14
    RIGHT_SHOULDER = 12
    RIGHT_HIP = 24
    RIGHT_KNEE = 26
    # RIGHT_ANKLE = 28
    # RIGHT_HEEL = 30

joints_to_track = [joint.value for joint in Joint]