import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os

class VideoPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualización de Datos y Video")
        self.video_path = None
        self.figures_paths = []

        # Botón para cargar el video
        self.load_button = tk.Button(self, text="Cargar Video", command=self.load_video)
        self.load_button.pack()

        # Canvas para mostrar el video procesado
        self.video_canvas = tk.Canvas(self, width=640, height=480)
        self.video_canvas.pack()

        # Menú desplegable para seleccionar gráficos
        self.graphs_menu = ttk.Combobox(self, state="readonly")
        self.graphs_menu.pack()
        self.graphs_menu.bind("<<ComboboxSelected>>", self.update_graph)

        # Espacio para los gráficos
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

    def load_video(self):
        self.video_path = filedialog.askopenfilename()
        if self.video_path:
            self.on_video_selected(self.video_path)

    def on_video_selected(self, video_path):
        # Este método será sobrescrito por el main.py
        pass

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

    def plot_data(self, figures_paths):
        self.figures_paths = figures_paths
        self.graphs_menu["values"] = self.figures_paths
        if self.figures_paths:
            self.graphs_menu.current(0)
            self.display_graph(self.figures_paths[0])

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.update_idletasks()
            self.update()

        cap.release()

    def on_closing(self):
        self.destroy()
