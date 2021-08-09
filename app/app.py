# Public libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from plot_plotly import plot
import pandas as pd
from cpfinder import cpfinder
from cpfinder.methods import online_changepoint_detection as oncd
from datetime import timedelta
from utils import *

# Custom Libraries
df = pd.read_csv("data.csv")
df = df[["datetime", "ts", "P", "E", "PF"]]
df["datetime"] = pd.to_datetime(df.datetime, infer_datetime_format=True)
min_date = df.datetime.min()
max_date = df.datetime.max()

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dcc.Graph(id="graph-with-slider"),
        dcc.Slider(
            id="date-slider",
            min=7,
            max=365,
            value=7,
            marks={
                7: {"label": "1 W", "style": {"color": "#17BECF"}},
                28: {"label": "4 W ", "style": {"color": "#17BECF"}},
                60: {"label": "2 M", "style": {"color": "#17BECF"}},
                120: {"label": "4 M ", "style": {"color": "#17BECF"}},
                240: {"label": "8 M", "style": {"color": "#17BECF"}},
                365: {"label": "1 Y", "style": {"color": "#17BECF"}},
            },
        ),
    ]
)


@app.callback(Output("graph-with-slider", "figure"), Input("date-slider", "value"))
def update_figure(selected_date):
    filtered_df = df.iloc[: (selected_date * 24), :]
    P = filtered_df.P
    dt = filtered_df.datetime
    hazard = 1 / 100
    model = oncd.GaussianUnknownMean(0, 1, 2)
    R, pmean, pvar = oncd.online_changepoint_detection(P, model, hazard, 1)
    fig = plot(P, dt, R, pmean, pvar)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8080, use_reloader=True)
