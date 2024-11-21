import os
import pandas as pd

from globals.video_analysis import VideoAnalysis
from globals.video_metadata import VideoMetadata
from pendulum.plot import plot_pendulum
from tracking.track_joints_to_pandas_csv import video_to_csv
from kinematic.joints_to_kinematics_data import JointsToKinematicsData
from constants.joints_ids_to_names import joints_to_track
from plotting.graphics_visualization import plot_joint_kinematics
from pendulum.model import Pendulum
from interfaz.user_interface import VideoPlayer

videos_dir = './resources/videos'
processed_videos_dir = './resources/processed_videos'
csv_dir = './resources/csv'
plots_dir = './resources/plots'

def get_videos_paths():
    files = os.listdir(videos_dir)
    return [os.path.join(videos_dir, file) for file in files]

def get_csv_path(path: str):
    csv_filename = os.path.basename(path).replace('.mov', '.csv')
    return os.path.join(csv_dir, csv_filename)

def get_output_video_path(path: str):
    video_filename = os.path.basename(path).replace('.mov', '_processed.mov')
    return os.path.join(processed_videos_dir, video_filename)

def process_videos(paths: list[str]):
    if not os.path.exists(processed_videos_dir):
        os.makedirs(processed_videos_dir)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    for path in paths:
        csv_path = get_csv_path(path)
        output_video_path = get_output_video_path(path)
        video_to_csv(path, csv_path, output_video_path)

def get_csv_paths():
    files = os.listdir(csv_dir)
    return [os.path.join(csv_dir, file) for file in files]

def build_kinematics_data() -> list[JointsToKinematicsData]:
    paths = get_csv_paths()
    return [JointsToKinematicsData(pd.read_csv(path), plots_dir + '/' + os.path.basename(path).split(".")[0]) for path in paths]

def process_kinematics_plots(joints_kinematics_data: list[JointsToKinematicsData]):
    for joints_kinematics in joints_kinematics_data:
        joint_ids = joints_to_track.keys()
        for joint_id in joint_ids:
            kinematics = joints_kinematics.get_joint(joint_id)
            plot_joint_kinematics(joint_id, kinematics, joints_kinematics.name)

def process_pendulum():
    for path in get_csv_paths():
        pendulum = Pendulum(pd.read_csv(path))
        plot_pendulum(pendulum, plots_dir + '/' + os.path.basename(path).split(".")[0] + '/pendulum.png')

def main():
    def on_video_selected(video_path):
        # Procesa el video seleccionado
        process_videos([video_path])
        kinematics_data = build_kinematics_data()
        process_kinematics_plots(kinematics_data)
        process_pendulum()

        df = pd.read_csv(get_csv_path(video_path))
        metadata = VideoMetadata((1920, 1080), 1/0.0019805559026734917)
        analysis = VideoAnalysis(metadata, df)
        print('Proceso finalizado')

        # Obtener rutas de los gráficos generados
        figures_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(plots_dir) for f in filenames if f.endswith('.png')]

        # Mostrar los gráficos generados
        app.video_analysis = analysis
        app.plot_data(figures_paths)

        # Reproduce el video procesado en la interfaz gráfica
        processed_video_path = get_output_video_path(video_path)
        app.show_processed_video(processed_video_path)

    # Lanza la interfaz gráfica para seleccionar el video
    app = VideoPlayer()
    app.on_video_selected = on_video_selected
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == '__main__':
    main()
