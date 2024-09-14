import cv2
import mediapipe as mp
import pandas as pd

mp_pose = mp.solutions.pose

# Insertar la dirección del video a analizar 
video_path = "../postura-project/video/Bien_Caminata_Con_Peso.mp4"
cap = cv2.VideoCapture(video_path)

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

# Articulaciones a trackear y sus números
joints_to_track = {
    28: "right_ankle",
    27: "left_ankle",
    24: "right_hip",
    23: "left_hip",
    16:  "right_wrist",
    15: "left_wrist",
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
            
            # Guardar los datos de las articulaciones con posiciones normalizadas
            data.append({
                'f': frame_number,     # Número de frame
                'a': joint_id,         # Número de la articulación
                'x': joint.x,          # Posición x (normalizada)
                'y': joint.y,          # Posición y (normalizada)
                'v': joint.visibility  # Visibilidad
            })

    frame_number += 1

cap.release()

# Crear DataFrame con los datos recolectados
df = pd.DataFrame(data)

# Multiplicar los valores de 'x' por el ancho y los de 'y' por el alto para desnormalizar
df['x_abs'] = df['x'] * resolution[0]
df['y_abs'] = df['y'] * resolution[1]

# Crear una nueva columna que indica el segundo en que se encuentra cada frame
df['second'] = df['f'] // fps

# Agrupar por cada segundo y calcular la media de las posiciones x e y para cada articulación
grouped_df = df.groupby(['second', 'a']).agg({
    'x_abs': 'mean',
    'y_abs': 'mean',
    'v': 'mean'  # También se puede calcular la visibilidad media
}).reset_index()

# Guardar el resultado en un nuevo archivo CSV
grouped_df.to_csv('joints_per_second.csv', index=False)

print("Archivo 'joints_per_second.csv' generado correctamente.")
