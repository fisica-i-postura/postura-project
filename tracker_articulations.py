import cv2
import mediapipe as mp
import pandas as pd

mp_pose = mp.solutions.pose

# Insertar la dirección del video a analizar 
cap = cv2.VideoCapture("../postura-project/video/Bien_Caminata_Con_Peso.mp4")

if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

data = []

pose = mp_pose.Pose(
    static_image_mode=False,
    min_tracking_confidence=0.5
)

# Articulaciones a trackear y sus números
joints_to_track = {
    28: "right_ankle",
    27: "left_ankle",
    24: "right_hip",
    23: "left_hip",
    16:  "right wrist",
    15: "left wrist",
    12: "right_shoulder",
    11: "left_shoulder"    
}

frame_number = 0 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        for joint_id, joint_name in joints_to_track.items():
            joint = results.pose_landmarks.landmark[joint_id]
            
            data.append({
                'f': frame_number,     # Número de frame
                'a': joint_id,         # Número de la articulación
                'x': joint.x,          # Posición x
                'y': joint.y,          # Posición y
                'v': joint.visibility  # Visibilidad
            })

    frame_number += 1 
cap.release()

df = pd.DataFrame(data)

df.to_csv('joints_coordinates.csv', index=False)

print("Archivo CSV generado correctamente.")
