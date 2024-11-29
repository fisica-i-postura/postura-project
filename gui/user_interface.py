from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from drawings.colors import Color
from drawings.draw_configs import JointDrawConfig, DrawType, DrawAxis
from drawings.draw_helper import DrawHelper
import matplotlib.pyplot as plt
from constants.joints_ids_to_names import joints_to_track
import webview

def get_draw_configs() -> list[JointDrawConfig]:
    return [
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.RED.value,trace=True),
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.X, color=Color.RED.value,trace=True),
        JointDrawConfig(joint_id=12, draw_type=DrawType.POSITION, draw_axis=DrawAxis.Y, color=Color.RED.value,trace=True),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.R, color=Color.BLUE.value,trace=True),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.X, color=Color.BLUE.value,trace=True),
        JointDrawConfig(joint_id=12, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.Y, color=Color.BLUE.value,trace=True),
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
        self.width = 853
        self.height = 480 
        self.fullscreen_graph = False

        #joints_to_track.clear()

        #joints_to_track.append()
        
        # Definir colores como variables de clas
        self.bg_color = '#1a2639'  # Azul marino
        self.button_color = '#3d5a80'  # Azul más claro para botones
        self.text_color = 'white'
        
        # Configurar el color de fondo de la ventana principal
        self.configure(bg=self.bg_color)
        
        # Configuración de la interfaz gráfica
        self.configure(bg=self.bg_color)
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                        fieldbackground=self.button_color,
                        background=self.button_color,
                        foreground=self.text_color,
                        selectbackground=self.button_color,
                        selectforeground=self.text_color,
                        padding=5)

        # Restante inicialización del layout
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
                                    width=self.width, 
                                    height=self.height,
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




######################################################################

         # Frame para gráficos (derecha)
        self.graph_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame para selección de gráficos
        self.graph_selection_frame = tk.Frame(self.graph_frame, bg=self.bg_color)
        self.graph_selection_frame.pack(fill=tk.X, pady=10)

        # Etiqueta para selector de gráficos
        self.graph_label = tk.Label(self.graph_selection_frame, 
                                    text="Seleccionar Gráfico:", 
                                    bg=self.bg_color, 
                                    fg=self.text_color)
        self.graph_label.pack(side=tk.LEFT, padx=10)

        # Combobox para seleccionar gráficos
        self.graph_combobox = ttk.Combobox(self.graph_selection_frame, 
                                           state="readonly", 
                                           style='Custom.TCombobox')
        self.graph_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        self.graph_combobox.bind('<<ComboboxSelected>>', self.update_graph)

        # Frame para imagen de gráfico
        self.image_frame = tk.Frame(self.graph_frame, bg=self.bg_color)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Label para mostrar gráfico PNG
        self.graph_image_label = tk.Label(self.image_frame, bg=self.bg_color)
        self.graph_image_label.pack(pady=10, expand=True)

        # Botón para expandir gráfico HTML
        self.expand_button = tk.Button(self.graph_frame, 
                                       text="Expandir", 
                                       command=self.expand_graph,
                                       bg=self.button_color, 
                                       fg=self.text_color,
                                       relief='raised', 
                                       borderwidth=0, 
                                       padx=20, 
                                       pady=10)
        self.expand_button.pack(pady=5)
        self.round_button(self.expand_button)

        # Lista para almacenar rutas de gráficos
        self.plot_paths = []
        self.current_html_path = None


##############################################


    def plot_data(self, plot_paths):
        """Actualiza la lista de gráficos disponibles"""
        self.plot_paths = list(plot_paths)
        graph_names = [path.stem for path in self.plot_paths]
        self.graph_combobox['values'] = graph_names
        
        # Seleccionar primer gráfico si está disponible
        if graph_names:
            self.graph_combobox.set(graph_names[0])
            self.update_graph()

    def update_graph(self, event=None):
        """Actualiza el gráfico mostrado según la selección"""
        selected_graph_name = self.graph_combobox.get()
        
        # Encontrar la ruta del PNG correspondiente
        png_path = next((path for path in self.plot_paths if path.stem == selected_graph_name), None)
        
        if png_path and png_path.exists():
            # Cargar y mostrar imagen
            img = Image.open(png_path)
            img_resized = img.resize((400, 300), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_resized)
            
            self.graph_image_label.configure(image=img_tk)
            self.graph_image_label.image = img_tk  # Mantener referencia
            
            # Buscar HTML correspondiente
            html_path = png_path.parent / f"{selected_graph_name}.html"
            self.current_html_path = str(html_path) if html_path.exists() else None

    def expand_graph(self):
        """Función para abrir el gráfico HTML interactivo"""
        if self.current_html_path and Path(self.current_html_path).exists():
            webview.create_window('Gráfico Interactivo', self.current_html_path)
            webview.start()
        else:
            tk.messagebox.showinfo("Información", "No hay gráfico HTML disponible.")


###############################################

    def round_button(self, button):
        """Aplica estilo redondeado a los botones"""
        button.bind('<Enter>', 
                   lambda e: button.configure(background='#4a6fa5'))
        button.bind('<Leave>', 
                   lambda e: button.configure(background=self.button_color))

    def load_video(self):
        self.video_path = filedialog.askopenfilename()
        if self.video_path:
            # Llamar a la función proporcionada para procesar el video
            if hasattr(self, 'on_video_selected'):
                self.on_video_selected(self.video_path)

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
            img = img.resize((self.width, self.height), Image.LANCZOS)
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
