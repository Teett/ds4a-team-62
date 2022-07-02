#libraries

from dash import Dash, html , dcc, dash_table, Input, Output, callback, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
import plotly.graph_objs as go
import plotly.express as px
from visualization import visualize
from components.data_requests.get_df import get_generate_df
from components.data_requests.data_transformation import transform_data
import pickle
import dash_daq as daq

# dash-labs plugin call, menu name and route
register_page(__name__, path='/analytics')

# Read the daily admissions on the database to pass to the graphs
daily_admissions = get_generate_df()


#bar_fig = visualize.ageband_plot(daily_admissions)
adm_dummies = transform_data(daily_admissions)

with open('../../models/admission/model_1_elastic_net_tunned.pickle', 'rb') as f:
    model = pickle.load(f)

try:
    y_prob =model.predict_proba(adm_dummies) 
    y_pred = (y_prob[:,1] >= 0.25).astype(int)
except:
    d = {'y_prob': 0}
    y_prob = pd.Series(data=d)


layout = html.Div(
    [   
        html.Div(dbc.Button("Update Data", id="update-data", color = "dark", n_clicks = 0)),
        html.Br(),
        html.H5("ER Insights:"),
        html.Br(),
        dbc.Container([
            dbc.Row(
                [
                dbc.Col(dcc.Graph(id = "age-band")),
                dbc.Col(daq.Gauge(
                        color={"gradient":True,"ranges":{"green":[0.7,1],"yellow":[0.4,0.7],"red":[0,0.4]}},
                        value= y_prob.mean().item(),
                        label='Probability of Hospitalization',
                        max=1,
                        min=0,
                        size = 300))
                ]
            ),
        dbc.Row(dcc.Graph(id = "corr-plot")), 
        dbc.Row([
            dbc.Col(dcc.Graph( id = 'ethnicity-plot')), 
            dbc.Col(dcc.Graph( id = 'acsc-plot'))
                ]
            )      
            ]
        )
    ]
)

@callback(
        Output("age-band", "figure"),
        Output("corr-plot", "figure"),
        Output("ethnicity-plot", "figure"),
        Output("acsc-plot", "figure"),
        Input('update-data','n_clicks'))
def update_plot (n):
    if n is None:
        return no_update
    else:
        daily_admissions = get_generate_df()
        age_fig = visualize.ageband_plot(daily_admissions)
        corr_fig = visualize.correlation_plot(daily_admissions)
        et_plot = visualize.ethnicity_plot(daily_admissions)
        acsc_plot = visualize.acsc_plot(daily_admissions)
        return age_fig, corr_fig, et_plot, acsc_plot