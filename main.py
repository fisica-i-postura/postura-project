from gui.user_interface import VideoPlayer
from globals.io.dataclasses import read_json_to_dataclass
from globals.io.paths import PathHelper, get_videos_folder_path
from globals.physics_processor import PhysicsProcessor
from globals.video_display import display
from pathlib import Path
from globals.user_input import UserInput



if __name__ == '__main__':
    app = VideoPlayer()

    # Modificar el método `load_video` para procesar el video seleccionado
    def on_video_selected(video_path):
        path_helper = PathHelper(Path(video_path))
        user_input_file = path_helper.get_user_input_path()

        # Verificar si el archivo de entrada de usuario existe
        if not user_input_file.exists():
            print(f"No se encontró el archivo de entrada para {video_path}.")
            return

        # Leer los datos de entrada del usuario y procesar el video
        user_input = read_json_to_dataclass(user_input_file, UserInput)
        user_input.video_path = video_path
        physics = PhysicsProcessor(user_input)

        # Actualizar la interfaz con el video procesado y gráficos
        app.video_analysis = physics.video_analysis
        app.show_processed_video(video_path)
        app.plot_data(list(path_helper.get_plots_folder_path().glob("*.png")))

    # Vincular el método al botón de carga
    app.on_video_selected = on_video_selected
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Manejar cierre limpio
    app.mainloop()
