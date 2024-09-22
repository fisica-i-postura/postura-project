import pandas as pd
import cv2

# Cargar el archivo CSV
df = pd.read_csv('joints_coordinates.csv')

# Cargar el video
video_path = "../postura-project/video/Bien_Caminata_Con_Peso.mp4"
video = cv2.VideoCapture(video_path)

# Obtener la resolución del video
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
resolution = (width, height)

# Calcular los fotogramas por segundo (FPS)
fps = video.get(cv2.CAP_PROP_FPS)

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
