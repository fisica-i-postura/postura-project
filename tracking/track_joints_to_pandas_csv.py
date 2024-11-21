import cv2
import mediapipe as mp
import pandas as pd
from constants.joints_ids_to_names import joints_to_track
from constants.df_columns_names import FRAME_INDEX, JOINT_ID, X_POSITION_NORMALIZED, Y_POSITION_NORMALIZED, VISIBILITY, \
    X_POSITION_ABSOLUTE, Y_POSITION_ABSOLUTE, SECOND, X_POSITION_IN_PX, Y_POSITION_IN_PX


# Función para calcular el factor de conversión (pixeles a metros)
def calculate_conversion_factor(real_distance_meters, pixel_distance):
    # Regla de tres simple: metros / píxeles
    meters_pixel_distance = real_distance_meters / pixel_distance
    print(f"Factor de conversión (metros/píxeles): {meters_pixel_distance}")
    return meters_pixel_distance

# Función para calcular la distancia en píxeles entre dos articulaciones
def calculate_pixel_distance(df, joint_a, joint_b):
    # Filtrar el DataFrame para obtener las posiciones de las articulaciones A y B
    joint_a_data = df[df[JOINT_ID] == joint_a]
    joint_b_data = df[df[JOINT_ID] == joint_b]

    # Calcular la distancia en píxeles entre A y B en el primer frame disponible
    x_a = joint_a_data.iloc[0][X_POSITION_IN_PX]
    y_a = joint_a_data.iloc[0][Y_POSITION_IN_PX]
    x_b = joint_b_data.iloc[0][X_POSITION_IN_PX]
    y_b = joint_b_data.iloc[0][Y_POSITION_IN_PX]

    # Distancia Euclidiana en píxeles
    pixel_distance = ((x_b - x_a) ** 2 + (y_b - y_a) ** 2) ** 0.5
    print(f"Distancia en píxeles entre las articulaciones {joint_a} y {joint_b}: {pixel_distance}")
    return pixel_distance


def video_to_csv(path: str, csv: str, output_video_path: str):

    #codigo hardcodeado momentaniamente 
    # tener en cuenta que las articulaciones que pongas en joint_a y joint_b
    # tienen que estar entre las articulaciones que se trackean, osea las que 
    # aparecen en el archivo joints_ids_to_names.py   
    joint_a = 16
    joint_b = 14
    real_distance_meters = 0.27


    cap = cv2.VideoCapture(path)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        min_tracking_confidence=0.5
    ) 

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

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, resolution)

    data = []       
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
                    FRAME_INDEX: frame_number,                  # Número de frame
                    JOINT_ID: joint_id,                         # Número de la articulación
                    X_POSITION_NORMALIZED: joint.x,             # Posición x (normalizada)
                    Y_POSITION_NORMALIZED: 1-joint.y,             # Posición y (normalizada)
                    VISIBILITY: joint.visibility                # Visibilidad
                })

                x_abs = int(joint.x * width)
                y_abs = int((1 - joint.y) * height)
                ##cv2.circle(frame, (x_abs, y_abs), 5, (0, 255, 0), -1)  # Círculo verde para cada landmark

            mp.solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        out.write(frame)
        frame_number += 1

    cap.release()

    # Crear DataFrame con los datos recolectados
    df = pd.DataFrame(data)    

    # Multiplicar los valores de 'x' por el ancho y los de 'y' por el alto para desnormalizar
    df[X_POSITION_IN_PX] = df[X_POSITION_NORMALIZED] * resolution[0]
    df[Y_POSITION_IN_PX] = df[Y_POSITION_NORMALIZED] * resolution[1]

    # Calcular la distancia en píxeles entre las articulaciones A y B
    pixel_distance = calculate_pixel_distance(df, joint_a, joint_b)

    # Calcular el factor de conversión utilizando la distancia real en metros
    conversion_factor = calculate_conversion_factor(real_distance_meters, pixel_distance)

    # Aplicar el factor de conversión para obtener los valores en metros
    df[X_POSITION_ABSOLUTE] = df[X_POSITION_IN_PX] * conversion_factor
    df[Y_POSITION_ABSOLUTE] = df[Y_POSITION_IN_PX] * conversion_factor

    # Crear una nueva columna que indica el segundo en que se encuentra cada frame
    df[SECOND] = df[FRAME_INDEX] / fps

    df.to_csv(csv, index=False)

    print(f"Archivo CSV '{csv}' y video procesado '{output_video_path}' generados correctamente.")