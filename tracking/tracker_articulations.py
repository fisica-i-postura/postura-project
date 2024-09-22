import cv2
import mediapipe as mp
import pandas as pd
from variables.joints_ids_to_names import joints_to_track
from variables.constants import FRAME_INDEX, JOINT_ID, X_POSITION_NORMALIZED, Y_POSITION_NORMALIZED, VISIBILITY, X_POSITION_ABSOLUTE, Y_POSITION_ABSOLUTE, SECOND

def video_to_csv(path: str, csv: str):
    cap = cv2.VideoCapture(path)
    mp_pose = mp.solutions.pose

    # Verificar si el video se pudo abrir
    if not cap.isOpened():
        print("Error: No se pudo abrir el video.")
        exit()

    # Obtener la resolución del video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    resolution = (width, height)

    # Calcular los fotogramas por segundo (FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)

    data = []

    pose = mp_pose.Pose(
        static_image_mode=False,
        min_tracking_confidence=0.5
    )    

    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            for joint_id in joints_to_track.keys():
                joint = results.pose_landmarks.landmark[joint_id]
                
                # Guardar los datos de las articulaciones con posiciones normalizadas
                data.append({
                    FRAME_INDEX: frame_number,      # Número de frame
                    JOINT_ID: joint_id,       # Número de la articulación
                    X_POSITION_NORMALIZED: joint.x,           # Posición x (normalizada)
                    Y_POSITION_NORMALIZED: joint.y,           # Posición y (normalizada)
                    VISIBILITY: joint.visibility  # Visibilidad
                })

        frame_number += 1

    cap.release()

    # Crear DataFrame con los datos recolectados
    df = pd.DataFrame(data)

    # Multiplicar los valores de 'x' por el ancho y los de 'y' por el alto para desnormalizar
    df[X_POSITION_ABSOLUTE] = df[X_POSITION_NORMALIZED] * resolution[0] / 1000
    df[Y_POSITION_ABSOLUTE] = df[Y_POSITION_NORMALIZED] * resolution[1] / 1000

    # Crear una nueva columna que indica el segundo en que se encuentra cada frame
    df[SECOND] = df[FRAME_INDEX] / fps

    df.to_csv(csv, index=False)

    print(f"Archivo '{csv}' generado correctamente.")