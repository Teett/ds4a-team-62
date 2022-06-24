#libraries

import dash
from dash import Dash, html , dcc, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
import base64
import datetime
import io
import plotly.graph_objs as go
import plotly.express as px


# dash-labs plugin call, menu name and route
register_page(__name__, path='/analytics')


layout = html.Div(
    [
        html.P("General Insights:"),
        html.Div(id="bar-container", children=[]),
    ]
)


# @callback(
#     [Output("bar-container", "children")]
#     [State("stored-data", "data")]
# )
# def make_graphs(data):
#     bar_fig = px.bar(data, x= data['Dimension'])
#     # print(data)
#     return dcc.Graph(figure=bar_fig)