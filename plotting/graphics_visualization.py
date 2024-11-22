import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Mapa de nombres de articulaciones
joint_names = {
    28: "Tobillo derecho",
    27: "Tobillo izquierdo",
    24: "Cadera derecha",
    23: "Cadera izquierda",
    16: "Muñeca derecha",
    15: "Muñeca izquierda",
    12: "Hombro derecho",
    11: "Hombro izquierdo",
    26: "Rodilla derecha",
    14: "Codo derecho",
}

# Crear la carpeta si no existe
directory = os.path.join(os.getcwd(), "resources/plots")
if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)

def plot_kinematics_continuous(time, data, smooth_data, confidence, ylabel, title, filename, out_dir=directory):

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    fig, ax = plt.subplots()

    # Revisar y manejar NaN/Inf en los datos
    if np.isnan(data).any() or np.isnan(smooth_data).any():
        print(f"Advertencia: NaN encontrado en los datos para {title}. El gráfico puede no ser preciso.")
    if np.isinf(data).any() or np.isinf(smooth_data).any():
        print(f"Advertencia: Inf encontrado en los datos para {title}. El gráfico puede no ser preciso.")

    # Crear los puntos (x, y) para la curva sin suavizado
    points = np.array([time, data]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Colores según confianza para la curva sin suavizado
    colors_raw = np.where(confidence[:-1] >= 0.5, 'blue', 'red')

    # Crear un LineCollection para la curva sin suavizado
    lc_raw = LineCollection(segments, colors=colors_raw, linewidth=2)
    ax.add_collection(lc_raw)

    # Crear los puntos (x, y) para la curva suavizada
    points_smooth = np.array([time, smooth_data]).T.reshape(-1, 1, 2)
    segments_smooth = np.concatenate([points_smooth[:-1], points_smooth[1:]], axis=1)

    # Colores para la curva suavizada (más claros para diferenciación)
    colors_smooth = np.where(confidence[:-1] >= 0.5, '#ADD8E6', '#FFB6C1')

    # Crear un LineCollection para la curva suavizada con líneas punteadas
    lc_smooth = LineCollection(segments_smooth, colors=colors_smooth, linewidth=2, linestyle='--')
    ax.add_collection(lc_smooth)

    # Usar np.nanmin y np.nanmax para evitar errores con NaN/Inf
    ax.set_xlim(time.min(), time.max())
    ax.set_ylim(np.nanmin([data, smooth_data]), np.nanmax([data, smooth_data]))

    # Etiquetas y título
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Añadir leyenda manualmente
    high_conf_raw = plt.Line2D([0], [0], color='blue', lw=2, label='Confianza >= 0.5 (Alta, sin suavizado)')
    low_conf_raw = plt.Line2D([0], [0], color='red', lw=2, label='Confianza < 0.5 (Baja, sin suavizado)')
    high_conf_smooth = plt.Line2D([0], [0], color='#ADD8E6', lw=2, linestyle='--', label='Confianza >= 0.5 (Alta, suavizado)')
    low_conf_smooth = plt.Line2D([0], [0], color='#FFB6C1', lw=2, linestyle='--', label='Confianza < 0.5 (Baja, suavizado)')

    # Mostrar la leyenda debajo del gráfico
    ax.legend(handles=[high_conf_raw, low_conf_raw, high_conf_smooth, low_conf_smooth], loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

    # Guardar el gráfico como PNG
    plt.savefig(os.path.join(out_dir, filename), bbox_inches='tight')
    plt.close()

def plot_joint_kinematics(joint_id, kinematics, output_dir=directory):
    # Posición X vs Tiempo
    plot_kinematics_continuous(
        kinematics.t, kinematics.x_position, kinematics.x_position_smooth, kinematics.p,
        ylabel="Posición X (m)",
        title=f"Articulación {joint_id} ({joint_names[joint_id]}): Posición X vs Tiempo",
        filename=f"joint_{joint_id}_x_position_vs_time.png",
        out_dir=output_dir
    )

    # Posición Y vs Tiempo
    plot_kinematics_continuous(
        kinematics.t, kinematics.y_position, kinematics.y_position_smooth, kinematics.p,
        ylabel="Posición Y (m)",
        title=f"Articulación {joint_id} ({joint_names[joint_id]}): Posición Y vs Tiempo",
        filename=f"joint_{joint_id}_y_position_vs_time.png",
        out_dir=output_dir
    )

    # Velocidad vs Tiempo
    plot_kinematics_continuous(
        kinematics.t, kinematics.velocity, kinematics.velocity_smooth, kinematics.p,
        ylabel="Velocidad (m/s)",
        title=f"Articulación {joint_id} ({joint_names[joint_id]}): Velocidad vs Tiempo",
        filename=f"joint_{joint_id}_velocity_vs_time.png",
        out_dir=output_dir
    )

    # Aceleración vs Tiempo
    plot_kinematics_continuous(
        kinematics.t, kinematics.accel, kinematics.accel_smooth, kinematics.p,
        ylabel="Aceleración (m/s²)",
        title=f"Articulación {joint_id} ({joint_names[joint_id]}): Aceleración vs Tiempo",
        filename=f"joint_{joint_id}_acceleration_vs_time.png",
        out_dir=output_dir
    )