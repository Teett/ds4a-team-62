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
import json


# dash-labs plugin call, menu name and route
register_page(__name__, path='/dashboard')

# from components.kpi.kpibadge import kpibadge

# kpi1 = kpibadge('325', 'Total kpi')
# kpi2 = kpibadge('1500', 'Total sales')
# kpi3 = kpibadge('325', 'Total transacciones')
# kpi4 = kpibadge('2122','Total User')


raw_er_admission = pd.read_excel('../../data/raw/er_admission.xlsx', sheet_name = 'Data')

ed_bed = raw_er_admission['ED bed occupancy'].mean()
arrival_intensity = raw_er_admission['Arrival intensity'].mean()
las_intensity = raw_er_admission['LAS intensity'].mean()
lwbs_intensity = raw_er_admission['LWBS intensity'].mean()

cards = [
    dbc.Card(
        [
            html.H2(f"{ed_bed:.2f}", className="card-title"),
            html.P("Average ED Bed Occupancy", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H2(f"{arrival_intensity:.2f}", className="card-title"),
            html.P("AVG Arrival within preceding hour", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2(f"{las_intensity:.2f}", className="card-title"),
            html.P("Ambulance Arrival Intensity", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2(f"{lwbs_intensity:.2f}", className="card-title"),
            html.P("LWBS intensity", className="card-text"),
        ],
        body=True,
        color="light",
    ),
]

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

layout = html.Div(
    [   dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        html.Br(),
        html.Div(id='output-datatable'),
        dbc.Container([
            dbc.Row([
                dbc.Col(id='output-div',   style = {'width': '50%'}),
                dbc.Col(id='output-div-2', style = {'width': '50%'}),
                    ]
                )
            ]
        )        
    ]
)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        # html.P("Inset X axis data"),
        # dcc.Dropdown(id='xaxis-data',
        #              options=[{'label':x, 'value':x} for x in df.columns]),
        # html.P("Inset Y axis data"),
        # dcc.Dropdown(id='yaxis-data',
        #              options=[{'label':x, 'value':x} for x in df.columns]),
        # html.Button(id="submit-button", children="Create Graph"),
        # html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),
        # print("diccionario",data)

        html.Hr(),  # horizontal line
        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@callback(Output('output-div', 'children'),
              Input('stored-data','data'))

def make_graphs(data):
    print(data)
    for dato in data:
        url = 'http://localhost:5000/insertar_admisions'
        myobj = dato
        myobj["nombreArchivo"] = "nombre_de_prueba"
        x = requests.post(url, json = myobj)
        print(x)
    url = 'http://localhost:5000/consulta_admision_por_nombre'
    myobj["nombreArchivo"] = "nombre_de_prueba"
    x = requests.post(url, json = myobj)
    print(x)
    print("json aja ", x.json())
    bar_fig = px.bar(data, x= 'Ethnicity')
    # print(data)
    return dcc.Graph(figure=bar_fig)

@callback(Output('output-div-2', 'children'),
              Input('stored-data','data'))
def make_graphs_2(data):
    bar_fig = px.bar(data, x= 'Gender')
    # print(data)
    return dcc.Graph(figure=bar_fig)