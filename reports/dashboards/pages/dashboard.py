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

myobj = {'ACSC': 'Search_Template',
 'Age_band': 'Search_Template',
 'Arr_Amb': 'Search_Template',
 'Arrival intensity': 'Search_Template',
 'Consultant_on_duty': 'Search_Template',
 'DayWeek_coded': 'Search_Template',
 'ED bed occupancy': 'Search_Template',
 'Ethnicity': 'Search_Template',
 'Gender': 'Search_Template',
 'IMD_quintile': 'Search_Template',
 'Inpatient_bed_occupancy': 'Search_Template',
 'LAS intensity': 'Search_Template',
 'LWBS intensity': 'Search_Template',
 'Last_10_mins': 'Search_Template',
 'Shift_coded': 'Search_Template',
 'Site': 'Search_Template'
 }


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

    [  

        dcc.Upload(
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

        html.Div(
        [
            dbc.Button("Save File in Database", id="submit-button", color = "primary", style={"margin-left": "15px"}, n_clicks = 0),
            dbc.Button("Read Last File", id="read-button", color = "secondary", style={"margin-left": "20px"}, n_clicks = 0),
            dbc.Button("Generate Insights", id="graph-button", color = "dark", style={"margin-left": "25px"}, n_clicks = 0),
                    ]
                ),
        html.Br(),
        html.Span(id="output-database", style={"verticalAlign": "middle"}),
        #dbc.Row([dbc.Col(card) for card in cards]), 
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
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),
        # print("diccionario",data)

        html.Hr(),  # horizontal line
        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
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


@callback(Output('output-database', 'children'),
          Input('submit-button','n_clicks'),
          State('stored-data','data'))
def save_in_db(n, data):
    print(data)
    if n is None:
        return dash.no_update
    else:
        for dato in data:
            url = 'http://localhost:5000/insertar_admisions'
            myobj = dato
            myobj["nombreArchivo"] = "nombre_de_prueba"
            x = requests.post(url, json = myobj)
            print(x)
        return f"Data saved in the Database"

    ###### Send chunks of data instead of 1 by 1 #####

    # url = 'http://localhost:5000/insertar_admisions'
    # data = pd.DataFrame(data)
    # data['nombreArchivo'] = 'nombre_de_prueba'
    # data = data.to_dict('records')
    # chunks = [data[x:x+10] for x in range(0, len(data), 30)]
    # for i, chunk in enumerate(chunks):
    #     r = requests.post(url, data = json.dumps(chunk), headers = {'content-type': 'application/json'})
    #     assert(r.status_code == 200), f'Error, status code is: {r.status_code}'
    #     print(f'total processed chunk {i+1}/{len(chunks)}')


@callback(Output('output-div', 'children'),
              State('stored-data','data'))
def make_graphs(data):
    bar_fig = px.bar(data, x= 'DayWeek_coded')
    # print(data)
    return dcc.Graph(figure=bar_fig)
    
@callback(Output('output-div-2', 'children'),
              Input('stored-data','data'))
def make_graphs_2(data):
    bar_fig = px.bar(data, x= 'Gender')
    # print(data)
    return dcc.Graph(figure=bar_fig)


@callback(Output('output-datatable', 'children'),
          Input('read-button','n_clicks'))
def read_db (n):
    if n is None:
        return dash.no_update
    else: 
        url = 'http://localhost:5000/consulta_admision_por_nombre'
        
        myobj = {'ACSC': 'Search_Template',
        'Age_band': 'Search_Template',
        'Arr_Amb': 'Search_Template',
        'Arrival intensity': 'Search_Template',
        'Consultant_on_duty': 'Search_Template',
        'DayWeek_coded': 'Search_Template',
        'ED bed occupancy': 'Search_Template',
        'Ethnicity': 'Search_Template',
        'Gender': 'Search_Template',
        'IMD_quintile': 'Search_Template',
        'Inpatient_bed_occupancy': 'Search_Template',
        'LAS intensity': 'Search_Template',
        'LWBS intensity': 'Search_Template',
        'Last_10_mins': 'Search_Template',
        'Shift_coded': 'Search_Template',
        'Site': 'Search_Template'
        }
        myobj["nombre"] = "nombre_de_prueba"
        response = requests.post(url, json = myobj)
        print(response)
        print("json aja ", response.json())
        response = response.json()
        raw_er_admission = pd.DataFrame.from_dict(data = response['Respuesta'])
        #raw_er_admission.drop(['Stay_length','Admission_ALL','createdAt','currentDate','id','nombreArchivo','updatedAt'], axis = 1, inplace = True)
        raw_er_admission.rename(columns = {'Inpatient_beoccupancy': 'Inpatient_bed_occupancy'}, inplace = True)
        return html.Div(
            dash_table.DataTable(
            data=raw_er_admission.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in raw_er_admission.columns],
            page_size=15)
        )




