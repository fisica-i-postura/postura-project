import cv2
import mediapipe as mp
import pandas as pd
from variables.joints_ids_to_names import joints_to_track
from variables.constants import FRAME, JOINT_ID, X_POS, Y_POS, VISIBILITY

def video_to_csv(path: str,csv: str):
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
            for joint_id in joints_to_track.items():
                joint = results.pose_landmarks.landmark[joint_id[0]]
                
                # Guardar los datos de las articulaciones con posiciones normalizadas
                data.append({
                    FRAME: frame_number,      # Número de frame
                    JOINT_ID: joint_id,       # Número de la articulación
                    X_POS: joint.x,           # Posición x (normalizada)
                    Y_POS: joint.y,           # Posición y (normalizada)
                    VISIBILITY: joint.visibility  # Visibilidad
                })

        frame_number += 1

    cap.release()

    # Crear DataFrame con los datos recolectados
    df = pd.DataFrame(data)

    # Multiplicar los valores de 'x' por el ancho y los de 'y' por el alto para desnormalizar
    df['x_abs'] = df[X_POS] * resolution[0]
    df['y_abs'] = df[Y_POS] * resolution[1]

    # Crear una nueva columna que indica el segundo en que se encuentra cada frame
    df['second'] = df[FRAME] // fps

    # Agrupar por cada segundo y calcular la media de las posiciones x e y para cada articulación
    grouped_df = df.groupby(['second', JOINT_ID]).agg({
        'x_abs': 'mean',
        'y_abs': 'mean',
        VISIBILITY: 'mean'  # También se puede calcular la visibilidad media
    }).reset_index()

    # Guardar el resultado en un nuevo archivo CSV
    grouped_df.to_csv(csv, index=False)

    print("Archivo 'joints_per_second.csv' generado correctamente.")

video_to_csv("../postura-project/video/Bien_Caminata_Con_Peso.mp4","joints_per_second.csv")