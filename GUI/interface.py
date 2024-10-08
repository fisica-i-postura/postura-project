import tkinter as tk
from tkinter import filedialog
import os

# Diccionario de articulaciones desde joints_ids_to_names.py
joints_to_track = {
    28: "right_ankle",
    27: "left_ankle",
    24: "right_hip",
    23: "left_hip",
    16: "right_wrist",
    15: "left_wrist",
    12: "right_shoulder",
    11: "left_shoulder"
}

# Función para seleccionar un archivo de video
def seleccionar_video(label_video):
    video_path = filedialog.askopenfilename(title="Seleccionar video", filetypes=[("Archivos de video", "*.mp4 *.avi *.mkv")])
    if video_path:
        label_video.config(text=os.path.basename(video_path))

# Crear la ventana principal
root = tk.Tk()
root.title("Comparación de Video Caminatas")
root.configure(bg='#2e2e2e')

# Frame superior
frame_superior = tk.Frame(root, bg='#2e2e2e')
frame_superior.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Subframe izquierdo para la selección y reproducción de video 1
frame_izquierdo = tk.Frame(frame_superior, bg='#3a3a3a', width=500, height=300)
frame_izquierdo.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Título para el Video 1
titulo_video1 = tk.Label(frame_izquierdo, text="Video 1", bg='#3a3a3a', fg='white', font=('Arial', 12, 'bold'))
titulo_video1.pack(pady=10)

# Botón para seleccionar video 1
boton_video1 = tk.Button(frame_izquierdo, text="Seleccionar Video 1", command=lambda: seleccionar_video(label_video1), bg='#4a4a4a', fg='white')
boton_video1.pack(pady=10)

# Label temporal para mostrar el nombre del video seleccionado 1
label_video1 = tk.Label(frame_izquierdo, text="Video 1 seleccionado", bg='#3a3a3a', fg='white')
label_video1.pack(pady=10)

# Subframe derecho para la selección y reproducción de video 2
frame_derecho = tk.Frame(frame_superior, bg='#3a3a3a', width=500, height=300)
frame_derecho.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Título para el Video 2
titulo_video2 = tk.Label(frame_derecho, text="Video 2", bg='#3a3a3a', fg='white', font=('Arial', 12, 'bold'))
titulo_video2.pack(pady=10)

# Botón para seleccionar video 2
boton_video2 = tk.Button(frame_derecho, text="Seleccionar Video 2", command=lambda: seleccionar_video(label_video2), bg='#4a4a4a', fg='white')
boton_video2.pack(pady=10)

# Label temporal para mostrar el nombre del video seleccionado 2
label_video2 = tk.Label(frame_derecho, text="Video 2 seleccionado", bg='#3a3a3a', fg='white')
label_video2.pack(pady=10)

# Frame inferior
frame_inferior = tk.Frame(root, bg='#2e2e2e')
frame_inferior.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Subframe inferior izquierdo (Gráfico del video 1)
grafico_video1 = tk.Frame(frame_inferior, bg='#3a3a3a', width=500, height=150)
grafico_video1.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Título para el gráfico del Video 1
titulo_grafico_video1 = tk.Label(grafico_video1, text="Gráfico del Video 1", bg='#3a3a3a', fg='white', font=('Arial', 12, 'bold'))
titulo_grafico_video1.pack(pady=10)

# Lista desplegable para seleccionar articulación (gráfico del Video 1)
label_articulacion_izq = tk.Label(grafico_video1, text="Seleccionar articulación (Video 1)", bg='#3a3a3a', fg='white')
label_articulacion_izq.pack(pady=10)
opcion_articulacion_izq = tk.StringVar(grafico_video1)
opcion_articulacion_izq.set("Seleccionar")  # Valor por defecto
dropdown_izq = tk.OptionMenu(grafico_video1, opcion_articulacion_izq, *joints_to_track.values())
dropdown_izq.pack(pady=10)

# Subframe inferior derecho (Gráfico del video 2)
grafico_video2 = tk.Frame(frame_inferior, bg='#3a3a3a', width=500, height=150)
grafico_video2.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

# Título para el gráfico del Video 2
titulo_grafico_video2 = tk.Label(grafico_video2, text="Gráfico del Video 2", bg='#3a3a3a', fg='white', font=('Arial', 12, 'bold'))
titulo_grafico_video2.pack(pady=10)

# Lista desplegable para seleccionar articulación (gráfico del Video 2)
label_articulacion_der = tk.Label(grafico_video2, text="Seleccionar articulación (Video 2)", bg='#3a3a3a', fg='white')
label_articulacion_der.pack(pady=10)
opcion_articulacion_der = tk.StringVar(grafico_video2)
opcion_articulacion_der.set("Seleccionar")  # Valor por defecto
dropdown_der = tk.OptionMenu(grafico_video2, opcion_articulacion_der, *joints_to_track.values())
dropdown_der.pack(pady=10)

# Iniciar la ventana
root.mainloop()
