from matplotlib.colors import LogNorm, Normalize
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def plot(data, dt, R, pmean, pvar, cps=[]):
    # shared_xaxes=True,
    fig = make_subplots(rows=2, cols=1, x_title="Date")
    fig.add_trace(
        go.Scatter(
            x=dt,
            y=data,
            name="Power",
            line=dict(color="firebrick", width=3),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dt,
            y=pmean,
            name="Predicted Mean",
            line=dict(color="black", width=1, dash="dot"),
        ),
        row=1,
        col=1,
    )
    _2std = 2 * np.sqrt(pvar)
    fig.add_trace(
        go.Scatter(
            x=dt,
            y=pmean - _2std,
            name="Predicted Mean - 2 std.",
            line=dict(color="black", width=1, dash="dot"),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=dt,
            y=pmean + _2std,
            name="Predicted Mean + 2 std.",
            line=dict(color="black", width=1, dash="dot"),
        ),
        row=1,
        col=1,
    )
    norm = LogNorm(vmin=0.0001, vmax=1)

    fig.add_trace(
        px.imshow((np.rot90(R)), binary_string=True).data[0],
        row=2,
        col=1,
    )
    fig.update_coloraxes(showscale=False)
    maxes = R.argmax(axis=1)

    # len(R) - maxes
    fig.add_trace(
        go.Scatter(
            x=dt,
            y=maxes,
            name="Maxes",
            line=dict(color="red", width=3),
        ),
        row=2,
        col=1,
    )

    fig.update_xaxes(range=[dt.min(), dt.max()])
    for cp in cps:
        fig.add_vline(
            x=dt.iloc[cp],
            line_width=1,
            line_dash="dot",
            line_color="red",
            row=2,
            col=1,
        )
        fig.add_vline(
            x=dt.iloc[cp],
            line_width=1,
            line_dash="dot",
            line_color="red",
            row=1,
            col=1,
        )

    fig.update_coloraxes(showscale=False)
    return fig
