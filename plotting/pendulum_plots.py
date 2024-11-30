from pathlib import Path

import numpy as np
from plotly.graph_objects import Figure
from plotly.io import write_image, write_html
from scipy.optimize import curve_fit

from pendulum.solid_bar_pendulum import SolidBarPendulum
from plotting.plots import plot_helper


# Definición de la función seno-coseno
def sin_cos_func(x, amplitude_sin, frequency_sin, phase_sin, amplitude_cos, frequency_cos, phase_cos, offset):
    return (amplitude_sin * np.sin(frequency_sin * x + phase_sin) +
            amplitude_cos * np.cos(frequency_cos * x + phase_cos) + offset)

# Ajuste de la curva seno-coseno
def fit_sin_cos(time, angle, pendulum: SolidBarPendulum):
    amplitude_guess = (np.max(angle) - np.min(angle)) / 2
    frequency_guess = np.mean(pendulum.angular_frequency)
    offset_guess = np.mean(angle)
    initial_guess = [amplitude_guess, frequency_guess, 0, amplitude_guess, frequency_guess, 0, offset_guess]
    params, covariance = curve_fit(sin_cos_func, time, angle, p0=initial_guess, maxfev=10000)
    return params

# Generar los datos ajustados
def generate_fit_data(x, params):
    return sin_cos_func(x, *params)

# Crear un gráfico superpuesto con datos originales y ajustados
def plot_with_fit(x, y, y_fit, path: Path, steps: int = 500):
    fig = Figure()

    # Datos originales
    fig.add_scatter(x=x, y=y, mode='lines', name='Original Data', line=dict(color='blue'))
    
    # Datos ajustados
    fig.add_scatter(x=x, y=y_fit, mode='lines', name='Fit Data', line=dict(color='red', dash='dash'))
    
    # Configuración del gráfico
    fig.update_layout(
        title="Shoulder-Wrist Angle with Sin-Cos Fit",
        xaxis_title="Time (s)",
        yaxis_title="Angle (degrees)",
        template="plotly_white"
    )
    
    # Guardar imágenes
    write_image(fig, f"{path}/angle_fit.png", width=1280, height=720, scale=4, engine="kaleido", format="png")
    write_html(fig, f"{path}/angle_fit.html")

# Integración con PendulumPlotHelper
class PendulumPlotHelper:
    def __init__(self, pendulum: SolidBarPendulum, steps: int, path: Path):
        self.pendulum = pendulum
        self.steps = steps
        self.path = path

    def plot(self):
        names = ["angle"]
        angle = np.degrees(np.arctan(np.tan(self.pendulum.angle)))
        time = self.pendulum.pivot.t
        
        # Gráfico original
        fig = plot_helper(
            time, [angle], names, "Shoulder-Wrist angle vs Time", 
            "Time (s)", "Angle (degrees)", steps=self.steps
        )
        write_image(fig, f"{self.path}/angle.png", width=1280, height=720, scale=4, engine="kaleido", format="png")
        write_html(fig, f"{self.path}/angle.html")

        # Ajuste de la curva y gráfico superpuesto
        params = fit_sin_cos(time, angle, self.pendulum)
        y_fit = generate_fit_data(time, params)
        plot_with_fit(time, angle, y_fit, self.path, steps=self.steps)
