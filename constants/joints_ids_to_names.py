from enum import Enum

import mediapipe as mp

# Mapping of joint ids to joint names
l = mp.solutions.pose.PoseLandmark

def get_joint_name(joint_id: int) -> str:
    return mp.solutions.pose.PoseLandmark(joint_id).name.lower().replace("_", " ").capitalize()

class Joint(Enum):    
    # Right side
    RIGHT_SHOULDER = 12
    RIGHT_ELBOW = 14
    RIGHT_WRIST = 16
    RIGHT_PINKY = 18
    RIGHT_INDEX = 20
    RIGHT_THUMB = 22
    RIGHT_HIP = 24
    RIGHT_KNEE = 26
    RIGHT_ANKLE = 28
    RIGHT_HEEL = 30
    RIGHT_FOOT_INDEX = 32

    #Left side
    LEFT_SHOULDER = 11
    LEFT_ELBOW = 13
    LEFT_WRIST = 15
    LEFT_PINKY = 17
    LEFT_INDEX = 19
    LEFT_THUMB = 21
    LEFT_HIP = 23
    LEFT_KNEE = 25
    LEFT_ANKLE = 27
    LEFT_HEEL = 29
    LEFT_FOOT_INDEX = 31


joints_to_track = []

class JointTracker:    
    def __init__(self):
        pass  # No es necesario inicializar nada aquí si no usas self.joints_to_track

    def add_joint(self, joint):
        global joints_to_track  # Declarar que vamos a usar la variable global
        if isinstance(joint, Joint) and joint.value not in joints_to_track:
            joints_to_track.append(joint.value)  # Modificar la lista global

    def remove_joint(self, joint):
        global joints_to_track  # Declarar que vamos a usar la variable global
        if joint.value in joints_to_track:
            joints_to_track.remove(joint.value)  # Modificar la lista global

    def get_joints(self):
        return joints_to_track  # Retornar la lista global