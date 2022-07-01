#libraries

from dash import Dash, html , dcc, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
import plotly.graph_objs as go
import plotly.express as px
from visualization.visualize import ageband_plot
from components.data_requests.get_df import get_generate_df
from components.data_requests.data_transformation import transform_data
import pickle
import dash_daq as daq

# dash-labs plugin call, menu name and route
register_page(__name__, path='/analytics')

# Read the daily admissions on the database to pass to the graphs

with open('../../models/admission/model_1_elastic_net_tunned.pickle', 'rb') as f:
    model = pickle.load(f)

daily_admissions = get_generate_df()
bar_fig = ageband_plot(daily_admissions)
adm_dummies = transform_data(daily_admissions)
y_prob =model.predict_proba(adm_dummies) 
y_pred = (y_prob[:,1] >= 0.25).astype(int)

# fig_2 = go.Figure(go.Indicator(
#             domain = {'x': [0, 1], 'y': [0, 1]},
#             value = {y_prob.mean().item()},
#             mode = "gauge+number+delta",
#             title = {'text': "Hospitalization Probability"},
#             delta = {'reference': 0.75}, #Goal of 75% of pacients that pass to hospitalization
#             gauge = {'axis': {'range': [None, 1.0]},
#                     'steps' : [
#                         {'range': [0, 0.30], 'color': "red"},
#                         {'range': [0.30, 0.70], 'color': "lightyellow"},
#                         {'range': [0.70, 1.0], 'color': "lightgreen"}],
#                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.85}}))

layout = html.Div(
    [
        html.P("General Insights:"),
        dcc.Graph(figure=bar_fig),
        #dcc.Graph(figure = fig_2),
        daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0.7,1],"yellow":[0.4,0.7],"red":[0,0.4]}},
            value=y_prob.mean().item(),
            label='Probability of Hospitalization',
            max=1,
            min=0,
        ),
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