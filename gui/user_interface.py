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
<<<<<<< Updated upstream
        self.width = 853
        self.height = 480 
        self.fullscreen_graph = False
=======
        self.width = 640
        self.height = 360 
>>>>>>> Stashed changes

        joints_to_track.clear()

        joints_to_track.append()
        
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
<<<<<<< Updated upstream
        self.load_button = tk.Button(self.video_frame, 
                                   text="Cargar Video",
=======
        self.load_button = tk.Button(self.load_joint_frame, 
                                   text="Upload Video",
>>>>>>> Stashed changes
                                   command=self.load_video,
                                   bg=self.button_color,
                                   fg=self.text_color,
                                   relief='raised',
                                   borderwidth=0,
                                   padx=20,
                                   pady=10)
<<<<<<< Updated upstream
        self.load_button.pack(pady=10)
        self.round_button(self.load_button)
=======
        self.load_button.pack(side=tk.LEFT)

        # Joint selection radio buttons
        self.joint_selection_var = tk.StringVar(value="right")
        
        self.right_joint_radio = tk.Radiobutton(
            self.load_joint_frame, 
            text="right joints", 
            variable=self.joint_selection_var, 
            value="right",
            bg=self.bg_color, 
            fg=self.text_color,
            selectcolor=self.button_color,
            activebackground=self.bg_color,
            activeforeground=self.text_color
        )
        self.right_joint_radio.pack(side=tk.LEFT, padx=5)

        self.left_joint_radio = tk.Radiobutton(
            self.load_joint_frame, 
            text="left joints", 
            variable=self.joint_selection_var, 
            value="left",
            bg=self.bg_color, 
            fg=self.text_color,
            selectcolor=self.button_color,
            activebackground=self.bg_color,
            activeforeground=self.text_color
        )
        self.left_joint_radio.pack(side=tk.LEFT, padx=5)
>>>>>>> Stashed changes

         # Checkbox para mostrar vectores
        self.vector_var = tk.BooleanVar()
        self.vector_checkbox = tk.Checkbutton(
            self.video_frame,
            text="Show Vectors",
            variable=self.vector_var,
            command=self.toggle_vectors,
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor=self.button_color,
            activebackground=self.bg_color,
            activeforeground=self.text_color
        )
        self.vector_checkbox.pack(pady=5)

<<<<<<< Updated upstream
=======
        # Botón para abrir el panel de selección de articulaciones
        self.select_joints_button = tk.Button(self.load_joint_frame, text="Select Joints", command=self.open_joint_selection_panel,
                                               bg=self.button_color, fg=self.text_color)
        self.select_joints_button.pack(padx=5)

        # Variables para almacenar el estado de las checkboxes
        self.joint_vars = {joint_id: tk.BooleanVar() for joint_id in 
                           [
                            12,
                            14,
                            16,
                            18,
                            20,
                            22,
                            24,
                            26,
                            28,
                            30,
                            32
                           ]
                           }

>>>>>>> Stashed changes
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

        # Frame para gráficos (derecha)
        self.graph_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

<<<<<<< Updated upstream
        # Frame para el primer gráfico
        self.graph1_frame = tk.Frame(self.graph_frame, bg=self.bg_color)
        self.graph1_frame.pack(fill=tk.BOTH, expand=True)
=======
        # Etiqueta para selector de gráficos
        self.graph_label = tk.Label(self.graph_selection_frame, 
                                    text="Select Graphics:", 
                                    bg=self.bg_color, 
                                    fg=self.text_color)
        self.graph_label.pack(side=tk.LEFT, padx=10, pady=10)
>>>>>>> Stashed changes

        # Menú desplegable para el primer gráfico
        self.graphs_menu1 = ttk.Combobox(self.graph1_frame, 
                                        state="readonly",
                                        style='Custom.TCombobox',
                                        width=40)
        self.graphs_menu1.pack(pady=10)
        self.graphs_menu1.bind("<<ComboboxSelected>>", 
                             lambda e: self.update_graph(e, 1))

<<<<<<< Updated upstream
        #### Canvas para el primer gráfico
        self.fig1, self.ax1 = plt.subplots(figsize=(8, 6))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.graph1_frame)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5)
        self.canvas1.get_tk_widget().bind("<Button-1>", lambda e: self.expand_graph(1))
=======
        # Botón de filtrado por articulación
        self.filter_button = tk.Button(self.graph_selection_frame, 
                                       text="filter", 
                                       command=self.show_joint_filter,
                                       bg=self.button_color, 
                                       fg=self.text_color,
                                       relief='raised', 
                                       borderwidth=0, 
                                       padx=10, 
                                       pady=5)
        self.filter_button.pack(side=tk.LEFT, padx=5)
        self.round_button(self.filter_button)
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
        #### Canvas para el segundo gráfico
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 6))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.graph2_frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5)
        self.canvas2.get_tk_widget().bind("<Button-1>", lambda e: self.expand_graph(2))
=======
        # Botón para expandir gráfico HTML
        self.expand_button = tk.Button(self.graph_frame, 
                                       text="Expand", 
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
        self.filtered_plot_paths = []
        self.current_joint_filter = None
 
############################################## 

    def open_joint_selection_panel(self):
        """Abre un panel para seleccionar las articulaciones."""
        selection_window = tk.Toplevel(self)
        selection_window.title("Seleccionar Articulaciones")
        selection_window.geometry("300x400")
        selection_window.configure(bg=self.bg_color)

        title_label = tk.Label(selection_window, text="Seleccionar Articulaciones", bg=self.bg_color, fg=self.text_color)
        title_label.pack(pady=10)

        # Crear checkbuttons para cada articulación
        for joint_id in sorted(self.joint_vars.keys()):
            cb = tk.Checkbutton(selection_window,
                                text=f"Joint {joint_id}",
                                variable=self.joint_vars[joint_id],
                                bg=self.bg_color,
                                fg=self.text_color,
                                selectcolor=self.button_color,
                                activebackground=self.bg_color)
            cb.pack(anchor=tk.W)

        # Botón para aplicar la selección
        apply_button = tk.Button(selection_window, text="Aplicar", command=lambda: self.apply_joint_selection(selection_window),
                                 bg=self.button_color, fg=self.text_color)
        apply_button.pack(pady=10)


    def apply_joint_selection(self, window):
        """Aplica la selección de articulaciones y cierra la ventana."""
        window.destroy()  # Cierra la ventana después de aplicar


    def get_draw_configs(self) -> list[JointDrawConfig]:
        """Genera las configuraciones de dibujo basadas en las articulaciones seleccionadas."""
        selected_joints = [joint_id for joint_id in self.joint_vars if self.joint_vars[joint_id].get()]
        
        draw_configs = []
        for joint_id in selected_joints:
            draw_configs.extend([
                JointDrawConfig(joint_id=joint_id, draw_type=DrawType.POSITION, draw_axis=DrawAxis.R, color=Color.RED.value, trace=True),
                JointDrawConfig(joint_id=joint_id, draw_type=DrawType.POSITION, draw_axis=DrawAxis.X, color=Color.RED.value, trace=False),
                JointDrawConfig(joint_id=joint_id, draw_type=DrawType.POSITION, draw_axis=DrawAxis.Y, color=Color.RED.value, trace=False),
                JointDrawConfig(joint_id=joint_id, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.R, color=Color.BLUE.value, trace=False),
                JointDrawConfig(joint_id=joint_id, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.X, color=Color.BLUE.value, trace=False),
                JointDrawConfig(joint_id=joint_id, draw_type=DrawType.VELOCITY, draw_axis=DrawAxis.Y, color=Color.BLUE.value, trace=False),
            ])
        
        return draw_configs
    

##############################################

    def update_joint_selection(self, event):
        selected_joint_id = int(self.joint_combobox.get())
        # Update draw_helper with new configurations based on selected joint
        self.draw_helper = DrawHelper(self.video_analysis, get_draw_configs(selected_joint_id))

    def plot_data(self, plot_paths):
        """Actualiza la lista de gráficos disponibles"""
        self.plot_paths = list(plot_paths)
        self.filtered_plot_paths = self.plot_paths
        self.update_graph_combobox()

    def update_graph_combobox(self):
        """Actualiza el combobox de gráficos"""
        graph_names = [path.stem for path in self.filtered_plot_paths]
        self.graph_combobox['values'] = graph_names
        
        # Seleccionar primer gráfico si está disponible
        if graph_names:
            self.graph_combobox.set(graph_names[0])
            self.update_graph()

    def show_joint_filter(self):
        """Muestra una ventana de filtrado por articulación"""
        filter_window = tk.Toplevel(self)
        filter_window.title("Filtrar Articulaciones")
        filter_window.geometry("300x550")
        filter_window.configure(bg=self.bg_color)

        # Centrar la ventana
        self.center_window(filter_window)

        # Título de la ventana de filtrado
        title_label = tk.Label(filter_window, 
                            text="Seleccionar Articulaciones", 
                            bg=self.bg_color, 
                            fg=self.text_color, 
                            font=("Arial", 12, "bold"))
        title_label.pack(pady=10)

        # Frame para contener los checkbuttons
        checkbox_frame = tk.Frame(filter_window, bg=self.bg_color)
        checkbox_frame.pack(expand=False, fill=tk.BOTH, padx=20)

        # Variables de control para los checkbuttons
        joint_vars = {}
        
        # Obtener articulaciones únicas de los nombres de archivos
        unique_joints = set()
        for path in self.plot_paths:
            parts = path.stem.split('_')
            if len(parts) > 0:
                unique_joints.add(parts[0])

        # Variable para seleccionar/deseleccionar todo
        select_all_var = tk.BooleanVar(value=True)

        # Checkbox de "Seleccionar Todo"
        select_all_cb = tk.Checkbutton(checkbox_frame, 
                                    text="Todo", 
                                    variable=select_all_var,
                                    command=lambda: self.toggle_all_joints(joint_vars, select_all_var),
                                    bg=self.bg_color, 
                                    fg=self.text_color,
                                    selectcolor=self.button_color,
                                    activebackground=self.bg_color)
        select_all_cb.pack(anchor=tk.W)

        # Crear checkbuttons para cada articulación
        for joint in sorted(unique_joints):
            # Usar un valor predeterminado basado en la selección de "Todo"
            var = tk.BooleanVar(value=select_all_var.get())
            joint_vars[joint] = var
            
            cb = tk.Checkbutton(checkbox_frame, 
                                text=joint, 
                                variable=var, 
                                bg=self.bg_color, 
                                fg=self.text_color,
                                selectcolor=self.button_color,
                                activebackground=self.bg_color,
                                command=lambda j=joint: self.update_select_all(joint_vars, select_all_var))
            cb.pack(anchor=tk.W)

        # Botón para aplicar filtro
        apply_button = tk.Button(filter_window, 
                                text="Aplicar Filtro", 
                                command=lambda: self.apply_joint_filter(joint_vars, filter_window),
                                bg=self.button_color, 
                                fg=self.text_color)
        apply_button.pack(pady=10)

    def center_window(self, window):
        """Centra una ventana en la pantalla"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_all_joints(self, joint_vars, select_all_var):
        """Selecciona o deselecciona todas las articulaciones"""
        for var in joint_vars.values():
            var.set(select_all_var.get())

    def update_select_all(self, joint_vars, select_all_var):
        """Actualiza el estado de 'Seleccionar Todo' basado en las selecciones individuales"""
        all_selected = all(var.get() for var in joint_vars.values())
        select_all_var.set(all_selected)

    def apply_joint_filter(self, joint_vars, filter_window):
        """Aplica el filtro de articulaciones y cierra la ventana"""
        # Filtrar gráficos basados en las articulaciones seleccionadas
        self.filtered_plot_paths = [
            path for path in self.plot_paths 
            if any(joint in path.stem and joint_vars[joint].get() 
                for joint in joint_vars.keys())
        ]

        # Actualizar el combobox
        self.update_graph_combobox()

        # Cerrar la ventana de filtrado
        filter_window.destroy()

    def update_graph(self, event=None):
        """Actualiza el gráfico mostrado según la selección"""
        selected_graph_name = self.graph_combobox.get()
        
        # Encontrar la ruta del PNG correspondiente
        png_path = next((path for path in self.filtered_plot_paths if path.stem == selected_graph_name), None)
        
        if png_path and png_path.exists():
            # Cargar y mostrar imagen
            img = Image.open(png_path)
            img_resized = img.resize((600, 400), Image.LANCZOS)
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
>>>>>>> Stashed changes

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


    def plot_data(self, figures_paths):
        self.figures_paths = [str(path) for path in figures_paths]  # Convertir Path a str
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
        ax = self.ax1 if graph_number == 1 else self.ax2
        canvas = self.canvas1 if graph_number == 1 else self.canvas2

        ax.clear()
        img = plt.imread(graph_path)
        ax.imshow(img)
        ax.axis('off')
        canvas.draw()

    def expand_graph(self, graph_number):
        """Expand the selected graph to full screen with a more robust approach."""
        # If already in fullscreen, restore original layout
        if self.fullscreen_graph:
            self.restore_layout()
            return

        # Set fullscreen flag
        self.fullscreen_graph = True

        # Determine which graph to expand
        if graph_number == 1:
            source_fig = self.fig1
            source_path = self.graphs_menu1.get()
        else:
            source_fig = self.fig2
            source_path = self.graphs_menu2.get()

        # Hide the main frame
        self.main_frame.pack_forget()

        # Create a new fullscreen frame
        self.fullscreen_frame = tk.Frame(self, bg=self.bg_color)
        self.fullscreen_frame.pack(fill=tk.BOTH, expand=True)

        # Create a new figure with the same size as the screen
        fullscreen_fig, fullscreen_ax = plt.subplots(figsize=(16, 9), dpi=100)
        fullscreen_canvas = FigureCanvasTkAgg(fullscreen_fig, master=self.fullscreen_frame)
        fullscreen_canvas_widget = fullscreen_canvas.get_tk_widget()
        fullscreen_canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Load and display the image
        img = plt.imread(source_path)
        fullscreen_ax.clear()
        fullscreen_ax.imshow(img)
        fullscreen_ax.axis('off')
        fullscreen_fig.tight_layout(pad=0)
        fullscreen_canvas.draw()

        # Add a return button
        return_button = tk.Button(
            self.fullscreen_frame, 
            text="Volver", 
            command=self.restore_layout,
            bg=self.button_color, 
            fg=self.text_color, 
            relief='raised', 
            borderwidth=0,
            padx=20, 
            pady=10
        )
        return_button.pack(side=tk.BOTTOM, pady=10)

    def restore_layout(self):
        """Restore the original layout after fullscreen."""
        # Destroy the fullscreen frame if it exists
        if hasattr(self, 'fullscreen_frame'):
            self.fullscreen_frame.destroy()
            del self.fullscreen_frame

        # Reset fullscreen flag
        self.fullscreen_graph = False

        # Restore the main frame
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Redraw original graphs to ensure they're displayed correctly
        if self.figures_paths:
            # Redisplay graphs from the original paths
            first_graph = self.figures_paths[0]
            second_graph = self.figures_paths[min(1, len(self.figures_paths) - 1)]
            
            self.display_graph(first_graph, 1)
            self.display_graph(second_graph, 2)

    def clear_layout(self):
        """Oculta temporalmente todos los elementos de la ventana."""
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    

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
