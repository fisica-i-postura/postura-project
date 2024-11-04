import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from threading import Thread
import os

class VideoPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualización de Datos y Video")
        self.video_path = None
        self.processed_video_path = None
        self.figures_paths = []
        self.current_image = None
        self.cap = None
        self.playing = False
        self.stop_playback = False

        # Frame principal para la distribución de video y gráfico
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Sub-frame para el video y sus controles (izquierda)
        self.video_frame = tk.Frame(self.main_frame)
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botón para cargar el video, arriba del video
        self.load_button = tk.Button(self.video_frame, text="Cargar Video", command=self.load_video)
        self.load_button.pack()

        # Canvas para mostrar el video procesado
        self.video_canvas = tk.Canvas(self.video_frame, width=640, height=480)
        self.video_canvas.pack()

        # Controles de reproducción dentro de video_frame
        self.control_frame = tk.Frame(self.video_frame)
        self.control_frame.pack()

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_video)
        self.stop_button.pack(side=tk.LEFT)

        # Barra de progreso dentro de video_frame
        self.progress = tk.Scale(self.video_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.seek_video)
        self.progress.pack(fill=tk.X, expand=True)

        # Sub-frame para gráficos y menú (derecha)
        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Menú desplegable para seleccionar gráficos
        self.graphs_menu = ttk.Combobox(self.graph_frame, state="readonly")
        self.graphs_menu.pack()
        self.graphs_menu.bind("<<ComboboxSelected>>", self.update_graph)

        # Espacio para los gráficos
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_video(self):
        self.video_path = filedialog.askopenfilename()
        if self.video_path:
            self.on_video_selected(self.video_path)

    def on_video_selected(self, video_path):
        self.processed_video_path = video_path
        self.show_processed_video(self.processed_video_path)

    def show_processed_video(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.progress.config(to=total_frames)
        self.current_frame = 0
        self.update_progress()

    def play_video(self):
        if self.cap is None or not self.cap.isOpened():
            return
        self.playing = True
        self.stop_playback = False
        self.update_progress()
        self.play()

    def play(self):
        if not self.playing or self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((640, 480), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.current_image = img_tk
            self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.progress.set(self.current_frame)
            self.after(33, self.play)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.playing = False

    def stop_video(self):
        self.playing = False
        self.stop_playback = True

    def seek_video(self, position):
        if self.cap is None:
            return
        frame_number = int(position)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((640, 480), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.current_image = img_tk
        self.current_frame = frame_number

    def plot_data(self, figures_paths):
        self.figures_paths = figures_paths
        self.graphs_menu["values"] = self.figures_paths
        if self.figures_paths:
            self.graphs_menu.current(0)
            self.display_graph(self.figures_paths[0])

    def update_graph(self, event=None):
        selected_graph = self.graphs_menu.get()
        if selected_graph:
            self.display_graph(selected_graph)

    def display_graph(self, graph_path):
        self.ax.clear()
        img = plt.imread(graph_path)
        self.ax.imshow(img)
        self.ax.axis('off')
        self.canvas.draw()

    def update_progress(self):
        if self.cap is not None and self.cap.isOpened() and self.playing:
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.progress.set(current_frame)
            self.after(100, self.update_progress)

    def on_closing(self):
        self.playing = False
        self.stop_playback = True
        if self.cap:
            self.cap.release()
        self.destroy()

# Inicialización de la interfaz
if __name__ == "__main__":
    app = VideoPlayer()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
