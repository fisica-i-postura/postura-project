import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pendulum.model import Pendulum

# Definición de la función seno + coseno para el ajuste
def sin_cos_func(x, amplitude_sin, frequency_sin, phase_sin, amplitude_cos, frequency_cos, phase_cos, offset):
    return amplitude_sin * np.sin(frequency_sin * x + phase_sin) + amplitude_cos * np.cos(frequency_cos * x + phase_cos) + offset

def plot_pendulum(pendulum: Pendulum, plot_path='resources/pendulum.png'):
    # Graficar los datos originales
    plt.plot(pendulum.time, pendulum.angle, label='Ángulo Original', color='blue')

    # Definir el rango de tiempo y el ángulo para el ajuste
    time_for_fit = pendulum.time
    angle_for_fit = pendulum.angle

    # Parámetros iniciales para el ajuste (ajustar manualmente si es necesario)
    initial_amplitude_sin = (np.max(angle_for_fit) - np.min(angle_for_fit)) / 2
    initial_amplitude_cos = initial_amplitude_sin
    initial_frequency = 2 * np.pi / (time_for_fit[-1] - time_for_fit[0])
    initial_phase = 0
    initial_offset = np.mean(angle_for_fit)

    # Realizar el ajuste con restricciones
    params, _ = curve_fit(
        sin_cos_func,
        time_for_fit,
        angle_for_fit,
        p0=[initial_amplitude_sin, initial_frequency, initial_phase, initial_amplitude_cos, initial_frequency, initial_phase, initial_offset],
        bounds=([0, 0, -2 * np.pi, 0, 0, -2 * np.pi, -np.inf], [np.inf, np.inf, 2 * np.pi, np.inf, np.inf, 2 * np.pi, np.inf])
    )

    # Generar valores ajustados
    angle_fit = sin_cos_func(time_for_fit, *params)

    # Graficar la curva ajustada
    plt.plot(time_for_fit, angle_fit, color='red', label='Ajuste Seno + Coseno', linestyle='--')

    # Configuración del gráfico
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo (deg)')
    plt.title('Ángulo Hombro-Muñeca vs. Tiempo')
    plt.legend()
    
    # Guardar y mostrar el gráfico
    plt.savefig(plot_path)
    plt.show()

    # Imprimir parámetros ajustados
    print("Parámetros ajustados:", params)

