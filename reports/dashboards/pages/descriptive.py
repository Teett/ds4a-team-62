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

layout = html.Div(
    [   
        html.Div(dbc.Button("Update Data", id="update-data", color = "dark", n_clicks = 0)),
        html.Br(),
        html.P('Note: if the page doesn´t upload with the latest data automatically, please click on the above button'),
        html.Br(),
        html.H3("ER Insights:"),
        html.Br(),
        html.Div([
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id = "age-band"),style = {'width' : '33%'}),
                    dbc.Col(dcc.Graph( id = 'ethnicity-plot'),style = {'width' : '33%'}),
                    dbc.Col(dcc.Graph( id = 'acsc-plot'),style = {'width' : '33%'})
                    ]),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph( id = 'ambulance-plot')),
                    dbc.Col(dcc.Graph( id = 'ambulance-shift'))
                ]
            ),
        html.Br(),
        # dbc.Row( 
        #     [   
        #         html.H4('Bed Occupancy and Ambulance Intensity in ER:'),
        #         dbc.Col(id = 'output-table')
        #     ]
        # ),
        html.Br(),
        dbc.Row(dcc.Graph(id = "corr-plot")),
            ]
        )
    ]
)

@callback(
        Output("age-band", "figure"),
        Output("corr-plot", "figure"),
        Output("ethnicity-plot", "figure"),
        Output("acsc-plot", "figure"),
        Output("ambulance-plot", "figure"),
        Output("ambulance-shift", "figure"),
        Output("ouput-table", "children"),
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
        # ambulance_plot = visualize.ambulance_ratio_week(daily_admissions)
        # ambulance_shift= daily_admissions.groupby('Shift_coded').mean()['LAS intensity'].to_frame().reset_index()
        # dict_shift = {0: 'Night', 1: 'Day'}
        # ambulance_shift = ambulance_shift.replace({'Shift_coded': dict_shift})
        # ambulance_shift = px.bar(ambulance_shift, x = 'LAS intensity', y ='Shift_coded', orientation = 'h', title = 'Ratio of arrivals by ambulance in each Shift')
        # ambulance_shift.update_layout( yaxis_title= "Shift", xaxis_title = 'Ambulance Arrival Intensity Ratio')
        # df_table = daily_admissions.groupby(['Site','DayWeek_coded','Shift_coded']).mean()[['Inpatient_bed_occupancy','LAS intensity','LWBS intensity']].reset_index()
        # table = dash_table.DataTable(
        #         data=df_table.to_dict('records'),
        #         columns=[{'name': i, 'id': i} for i in df_table.columns],
        #         page_size=5
        #     ),       
        return age_fig, corr_fig, et_plot, acsc_plot#, ambulance_plot, ambulance_shift, table 