import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from threading import Thread
import os

from drawings.colors import Color
from drawings.draw_configs import JointDrawConfig, DrawType, DrawAxis
from drawings.draw_helper import DrawHelper

def get_draw_configs() -> list[JointDrawConfig]:
    return [
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.RED.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.X, color=Color.RED.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.Y, color=Color.RED.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.R, color=Color.BLUE.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.X, color=Color.BLUE.value),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.Y, color=Color.BLUE.value),
    ]

def x(joints: list[int], types: list[DrawType], axes: list[DrawAxis]) -> list[JointDrawConfig]:
    return [JointDrawConfig(joint_id=joint, draw_type=draw_type, draw_axis=axis, color=Color.RED.value) for joint in joints for draw_type in types for axis in axes]

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
        self.video_analysis = None
        self.draw_helper = None
        self.show_vectors = False
        self.current_frame_data = None  # Almacena el frame actual   

        
        # Definir colores como variables de clase
        self.bg_color = '#1a2639'  # Azul marino
        self.button_color = '#3d5a80'  # Azul más claro para botones
        self.text_color = 'white'
        
        # Configurar el color de fondo de la ventana principal
        self.configure(bg=self.bg_color)
        
        # Estilo para los combobox
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                       fieldbackground=self.button_color,
                       background=self.button_color,
                       foreground=self.text_color,
                       selectbackground=self.button_color,
                       selectforeground=self.text_color,
                       padding=5)
        
        # Frame principal
        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame para el video (izquierda)
        self.video_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botón para cargar video
        self.load_button = tk.Button(self.video_frame, 
                                   text="Cargar Video",
                                   command=self.load_video,
                                   bg=self.button_color,
                                   fg=self.text_color,
                                   relief='raised',
                                   borderwidth=0,
                                   padx=20,
                                   pady=10)
        self.load_button.pack(pady=10)
        self.round_button(self.load_button)

         # Checkbox para mostrar vectores
        self.vector_var = tk.BooleanVar()
        self.vector_checkbox = tk.Checkbutton(
            self.video_frame,
            text="Mostrar Vectores",
            variable=self.vector_var,
            command=self.toggle_vectors,
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor=self.button_color,
            activebackground=self.bg_color,
            activeforeground=self.text_color
        )
        self.vector_checkbox.pack(pady=5)

        # Canvas para el video
        self.video_canvas = tk.Canvas(self.video_frame, 
                                    width=1280, 
                                    height=720,
                                    bg='black',
                                    highlightthickness=0)
        self.video_canvas.pack(pady=10)

        # Frame para controles
        self.control_frame = tk.Frame(self.video_frame, bg=self.bg_color)
        self.control_frame.pack(pady=10)

         # Botones de control
        self.play_button = tk.Button(self.control_frame, 
                                   text="Play",
                                   command=self.play_video,
                                   bg=self.button_color,
                                   fg=self.text_color,
                                   relief='raised',
                                   borderwidth=0,
                                   padx=20,
                                   pady=5)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.round_button(self.play_button)

        self.stop_button = tk.Button(self.control_frame, 
                                   text="Stop",
                                   command=self.stop_video,
                                   bg=self.button_color,
                                   fg=self.text_color,
                                   relief='raised',
                                   borderwidth=0,
                                   padx=20,
                                   pady=5)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.round_button(self.stop_button)

        # Barra de progreso
        self.progress = tk.Scale(self.video_frame, 
                               from_=0, 
                               to=100, 
                               orient=tk.HORIZONTAL,
                               command=self.seek_video,
                               bg=self.bg_color,
                               fg=self.text_color,
                               troughcolor=self.button_color,
                               highlightthickness=0)
        self.progress.pack(fill=tk.X, expand=True, padx=10)

        # Frame para gráficos (derecha)
        self.graph_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame para el primer gráfico
        self.graph1_frame = tk.Frame(self.graph_frame, bg=self.bg_color)
        self.graph1_frame.pack(fill=tk.BOTH, expand=True)

        # Menú desplegable para el primer gráfico
        self.graphs_menu1 = ttk.Combobox(self.graph1_frame, 
                                        state="readonly",
                                        style='Custom.TCombobox',
                                        width=40)
        self.graphs_menu1.pack(pady=10)
        self.graphs_menu1.bind("<<ComboboxSelected>>", 
                             lambda e: self.update_graph(e, 1))

        # Canvas para el primer gráfico
        self.fig1, self.ax1 = plt.subplots(figsize=(6, 4))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.graph1_frame)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5)

        # Frame para el segundo gráfico
        self.graph2_frame = tk.Frame(self.graph_frame, bg=self.bg_color)
        self.graph2_frame.pack(fill=tk.BOTH, expand=True)

        # Menú desplegable para el segundo gráfico
        self.graphs_menu2 = ttk.Combobox(self.graph2_frame, 
                                        state="readonly",
                                        style='Custom.TCombobox',
                                        width=40)
        self.graphs_menu2.pack(pady=10)
        self.graphs_menu2.bind("<<ComboboxSelected>>", 
                             lambda e: self.update_graph(e, 2))

        # Canvas para el segundo gráfico
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 4))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.graph2_frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5)

    def round_button(self, button):
        """Aplica estilo redondeado a los botones"""
        button.bind('<Enter>', 
                   lambda e: button.configure(background='#4a6fa5'))
        button.bind('<Leave>', 
                   lambda e: button.configure(background=self.button_color))

    def load_video(self):
        self.video_path = filedialog.askopenfilename()
        if self.video_path:
            self.on_video_selected(self.video_path)

    def plot_data(self, figures_paths):
        self.figures_paths = figures_paths
        # Configurar ambos menús desplegables con las mismas opciones
        self.graphs_menu1["values"] = self.figures_paths
        self.graphs_menu2["values"] = self.figures_paths
        
        if self.figures_paths:
            # Establecer valores iniciales diferentes para cada gráfico
            self.graphs_menu1.current(0)
            self.graphs_menu2.current(min(1, len(self.figures_paths) - 1))
            self.display_graph(self.figures_paths[0], 1)
            self.display_graph(self.figures_paths[min(1, len(self.figures_paths) - 1)], 2)

    def update_graph(self, event, graph_number):
        selected_graph = self.graphs_menu1.get() if graph_number == 1 else self.graphs_menu2.get()
        if selected_graph:
            self.display_graph(selected_graph, graph_number)

    def display_graph(self, graph_path, graph_number):
        if graph_number == 1:
            self.ax1.clear()
            img = plt.imread(graph_path)
            self.ax1.imshow(img)
            self.ax1.axis('off')
            self.canvas1.draw()
        else:
            self.ax2.clear()
            img = plt.imread(graph_path)
            self.ax2.imshow(img)
            self.ax2.axis('off')
            self.canvas2.draw()

    def show_processed_video(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.progress.config(to=total_frames)
        self.current_frame = 0
        self.update_progress()

    def play_video(self):
        self.draw_helper = DrawHelper(self.video_analysis, get_draw_configs())
        if self.cap is None or not self.cap.isOpened():
            return
        self.playing = True
        self.stop_playback = False
        self.update_progress()
        self.play()

    def play(self):
        if not self.playing or self.cap is None:
            return

        if self.update_frame():
            self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.progress.set(self.current_frame)
            self.after(33, self.play)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.playing = False    

    def stop_video(self):
        self.playing = False
        self.stop_playback = True
        # Asegurarse de que el último frame se muestre correctamente
        self.redraw_current_frame()

    # def seek_video(self, position):
    #     if self.cap is None:
    #         return
    #     frame_number = int(position)
    #     self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    #     ret, frame = self.cap.read()
    #     if ret:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         img = Image.fromarray(frame)
    #         img = img.resize((1280, 720), Image.LANCZOS)
    #         img_tk = ImageTk.PhotoImage(img)
    #         self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    #         self.current_image = img_tk
    #     self.current_frame = frame_number

    def seek_video(self, position):
        if self.cap is None:
            return
        frame_number = int(position)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.update_frame()
        self.current_frame = frame_number

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

    def toggle_vectors(self):
        """Cambia entre mostrar y ocultar vectores"""
        self.show_vectors = self.vector_var.get()
        # Redibujar el frame actual con o sin vectores
        self.redraw_current_frame()

    def get_frame(self):
        """Obtiene un nuevo frame del video"""
        if self.cap is None:
            return None, False

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame_data = frame.copy()  # Guardamos una copia del frame actual
        return frame, ret
    
    def draw_vectors_on_frame(self, frame):
        """Dibuja los vectores en el frame si están activados"""
        if self.show_vectors and self.draw_helper is not None:
            current_frame_idx = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
            frame_copy = frame.copy()
            self.draw_helper.draw(frame_copy, current_frame_idx)
            return frame_copy
        return frame
    
    def display_frame(self, frame):
        """Muestra el frame en el canvas"""
        if frame is not None:
            img = Image.fromarray(frame)
            img = img.resize((1280, 720), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.current_image = img_tk

    def redraw_current_frame(self):
        """Redibuja el frame actual con o sin vectores"""
        if self.current_frame_data is not None:
            frame = self.current_frame_data.copy()
            frame = self.draw_vectors_on_frame(frame)
            self.display_frame(frame)


    def update_frame(self):
        """Actualiza el frame actual con o sin vectores"""
        frame, ret = self.get_frame()
        if not ret:
            return False

        frame = self.draw_vectors_on_frame(frame)
        self.display_frame(frame)
        return True

    # def update_frame(self):
    #     """Actualiza el frame actual con o sin vectores"""
    #     if self.cap is None:
    #         return False

    #     ret, frame = self.cap.read()
    #     if not ret:
    #         return False

    #     # Convertir frame a RGB
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #     # Si los vectores están activados y tenemos el draw_helper
    #     if self.show_vectors and self.draw_helper is not None:
    #         current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
    #         self.draw_helper.draw(frame, current_frame)

    #     # Redimensionar y mostrar el frame
    #     img = Image.fromarray(frame)
    #     img = img.resize((1280, 720), Image.LANCZOS)
    #     img_tk = ImageTk.PhotoImage(img)
    #     self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    #     self.current_image = img_tk
    #     return True
    

    #853x480