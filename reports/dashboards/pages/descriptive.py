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
import requests
from visualization.visualize import ageband_plot

# Read the daily admissions on the database
url = 'http://localhost:5000/consulta_admisiones_de_hoy'
response = requests.get(url)
print(response)
print("json aja ", response.json())

response = response.json()
daily_admissions = pd.DataFrame.from_dict(data = response['Respuesta'])
daily_admissions.drop(['Stay_length','Admission_ALL','createdAt','currentDate','id','nombreArchivo','updatedAt'], axis = 1, inplace = True)
daily_admissions.rename(columns = {'Inpatient_beoccupancy': 'Inpatient_bed_occupancy'}, inplace = True)

daily_admissions = daily_admissions.astype({"ACSC": float,
                                            "Age_band": float,
                                            "Ethnicity": float,
                                            "Site": float,
                                            "IMD_quintile": float,
                                            "DayWeek_coded": int,
                                            "Shift_coded": int,
                                            "Arr_Amb": int,
                                            "Gender": int,
                                            "Consultant_on_duty": int,
                                            "ED bed occupancy": float,
                                            "Inpatient_bed_occupancy": float,
                                            "Arrival intensity": int,
                                            "LAS intensity": float,
                                            "LWBS intensity": float,
                                            "Last_10_mins": int})

print(daily_admissions.head())
print(type(daily_admissions.head()))

# dash-labs plugin call, menu name and route
register_page(__name__, path='/analytics')

bar_fig = ageband_plot(daily_admissions)

layout = html.Div(
    [
        html.P("General Insights:"),
        dcc.Graph(figure=bar_fig),
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