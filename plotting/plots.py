import numpy as np
import plotly.graph_objects as go


def plot_helper(x: np.ndarray, ys: list[np.ndarray], names:list[str], title: str, x_label: str, y_label: str, mode: str = 'lines') -> go.Figure:
    fig = go.Figure()
    for y, name in zip(ys, names):
        fig.add_trace(go.Scatter(x=x, y=y, mode=mode, name=name))
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    return fig