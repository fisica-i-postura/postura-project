import numpy as np
import plotly.graph_objects as go


def plot_helper(x: np.ndarray, ys: list[np.ndarray], names:list[str], title: str, x_label: str, y_label: str, mode: str = 'lines', steps: np.ndarray = np.array([])) -> go.Figure:
    fig = go.Figure()
    for y, name in zip(ys, names):
        fig.add_trace(go.Scatter(x=x, y=y, mode=mode, name=name))
        for step in steps:
            fig.add_shape(
                type="line",
                x0=x[step], y0=0,
                x1=x[step], y1=1,
                xref="x", yref="paper",
                line=dict(color="green", width=2, dash="dash")
            )
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    return fig