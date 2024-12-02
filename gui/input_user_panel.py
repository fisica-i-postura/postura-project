import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import json
from dataclasses import dataclass
from enum import Enum

from globals.io.paths import PathHelper

class Gender(Enum):
    MALE = 'M'
    FEMALE = 'F'

@dataclass
class UserInput:
    video_path: str
    joints_distance_in_meters: float = 0.33
    shoulder_wrist_distance_in_meters: float = 0.63  # Nuevo parámetro
    subject_gender: Gender = Gender.MALE
    subject_weight: float = 85.0

class UserInputDialog(tk.Toplevel):
    def __init__(self, parent, video_path):
        super().__init__(parent)
        self.title("Información del Sujeto")
        self.video_path = video_path
        self.result = None
        self.geometry("400x600")  # Ajustar la altura para incluir el nuevo campo
        self.configure(bg=parent.bg_color)
        self.resizable(False, False)

        # Centrar la ventana
        self.center_window()

        # Frame principal
        main_frame = tk.Frame(self, bg=parent.bg_color)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Título
        title_label = tk.Label(main_frame, 
                               text="Ingrese Información del Sujeto", 
                               bg=parent.bg_color, 
                               fg=parent.text_color, 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))

        # Distancia entre articulaciones
        distance_frame = tk.Frame(main_frame, bg=parent.bg_color)
        distance_frame.pack(fill=tk.X, pady=10)
        
        distance_label = tk.Label(distance_frame, 
                                  text="Distancia entre articulaciones (m):", 
                                  bg=parent.bg_color, 
                                  fg=parent.text_color)
        distance_label.pack(side=tk.LEFT)
        
        self.distance_entry = tk.Entry(distance_frame, 
                                       bg=parent.button_color, 
                                       fg=parent.text_color, 
                                       insertbackground=parent.text_color)
        self.distance_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        self.distance_entry.insert(0, "0.33")

        # Distancia hombro-muñeca (nuevo campo)
        wrist_distance_frame = tk.Frame(main_frame, bg=parent.bg_color)
        wrist_distance_frame.pack(fill=tk.X, pady=10)

        wrist_distance_label = tk.Label(wrist_distance_frame,
                                        text="Distancia hombro-muñeca (m):",
                                        bg=parent.bg_color,
                                        fg=parent.text_color)
        wrist_distance_label.pack(side=tk.LEFT)

        self.wrist_distance_entry = tk.Entry(wrist_distance_frame,
                                             bg=parent.button_color,
                                             fg=parent.text_color,
                                             insertbackground=parent.text_color)
        self.wrist_distance_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        self.wrist_distance_entry.insert(0, "0.63")  # Valor por defecto

        # Género
        gender_frame = tk.Frame(main_frame, bg=parent.bg_color)
        gender_frame.pack(fill=tk.X, pady=10)
        
        gender_label = tk.Label(gender_frame, 
                                text="Género:", 
                                bg=parent.bg_color, 
                                fg=parent.text_color)
        gender_label.pack(side=tk.LEFT)
        
        self.gender_var = tk.StringVar(value="M")
        male_radio = tk.Radiobutton(gender_frame, 
                                    text="Masculino", 
                                    variable=self.gender_var, 
                                    value="M", 
                                    bg=parent.bg_color, 
                                    fg=parent.text_color,
                                    selectcolor=parent.button_color)
        male_radio.pack(side=tk.LEFT)
        
        female_radio = tk.Radiobutton(gender_frame, 
                                      text="Femenino", 
                                      variable=self.gender_var, 
                                      value="F", 
                                      bg=parent.bg_color, 
                                      fg=parent.text_color,
                                      selectcolor=parent.button_color)
        female_radio.pack(side=tk.LEFT)

        # Peso
        weight_frame = tk.Frame(main_frame, bg=parent.bg_color)
        weight_frame.pack(fill=tk.X, pady=10)
        
        weight_label = tk.Label(weight_frame, 
                                text="Peso (kg):", 
                                bg=parent.bg_color, 
                                fg=parent.text_color)
        weight_label.pack(side=tk.LEFT)
        
        self.weight_entry = tk.Entry(weight_frame, 
                                     bg=parent.button_color, 
                                     fg=parent.text_color, 
                                     insertbackground=parent.text_color)
        self.weight_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        self.weight_entry.insert(0, "85")

        # Botón Confirmar
        confirm_button = tk.Button(main_frame,
                                   text="Confirmar",
                                   command=self.on_confirm,
                                   bg=parent.button_color,
                                   fg=parent.text_color)
        confirm_button.pack(pady=20)

        # Modal
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_confirm(self):
        """Validar y guardar los datos ingresados"""
        try:
            # Validar distancia entre articulaciones
            distance = float(self.distance_entry.get())
            if distance <= 0:
                raise ValueError("La distancia entre articulaciones debe ser mayor que 0")

            # Validar distancia hombro-muñeca
            wrist_distance = float(self.wrist_distance_entry.get())
            if wrist_distance <= 0:
                raise ValueError("La distancia hombro-muñeca debe ser mayor que 0")

            # Validar peso
            weight = float(self.weight_entry.get())
            if weight <= 0:
                raise ValueError("El peso debe ser mayor que 0")

            # Crear diccionario de entrada de usuario
            user_input_dict = {
                "video_path": self.video_path,
                "shoulder_elbow_distance_in_meters": distance,  # Asegúrate de usar el nombre correcto aquí
                "shoulder_wrist_distance_in_meters": wrist_distance,
                "subject_gender": self.gender_var.get(),
                "subject_weight": weight
            }

            # Guardar como JSON
            path_helper = PathHelper(Path(self.video_path))
            user_input_file = path_helper.get_user_input_path()
            
            with open(user_input_file, 'w') as f:
                json.dump(user_input_dict, f, indent=4)

            # Almacenar resultado para devolución
            self.result = user_input_dict
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))