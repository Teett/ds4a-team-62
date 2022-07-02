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
from components.kpi.kpibadge import kpibadge
from components.data_requests.get_df import get_generate_df
from components.data_requests.data_transformation import transform_data
import pickle
import dash_daq as daq


# dash-labs plugin call, menu name and route
register_page(__name__, path='/')

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

#Load the model to showw results in Insights:

with open('../../models/admission/model_1_elastic_net_tunned.pickle', 'rb') as f:
    model = pickle.load(f)

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
            #dbc.Button("Read Last File", id="read-button", color = "secondary", style={"margin-left": "20px"}, n_clicks = 0),
            dbc.Button("Generate Today's Insights", id="graph-button", color = "dark", style={"margin-left": "18px"}, n_clicks = 0),
                    ]
                ),
        html.Br(),
        html.Span(id="output-database", style={"verticalAlign": "middle"}), 
        html.Br(),
        html.Hr(),
        dbc.Container([
            html.H4(id= "output-title"),
            dbc.Row(id = "output-cards"),
            html.Br(),
            html.H4(id= "output-title-2"),
            dbc.Row(id ='output-badges'),
            html.Br(),
            #html.Div(id ='output-div')
            dbc.Row([
                dbc.Col(id='output-div',   style = {'width': '50%'}),
                dbc.Col(id='output-div-2', style = {'width': '50%'}),
                    ]
                )
            ]
        ),
        html.Div(id='output-datatable'),
        html.Br(),        
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
            html.H4('This is a preview of the file you uploaded'),
            html.H5('Note: If want to include this data in the Calculated Insights for Today, please firt save the file in the DataBase'),
            html.H5(f"File uploaded: {filename}"),
            html.H6(f"Date:{datetime.datetime.fromtimestamp(date)}"),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=5
            ),
            dcc.Store(id='stored-data', data=df.to_dict('records')),
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
        # for dato in data:
        #     url = 'http://localhost:5000/insertar_admisions'
        #     myobj = dato
        #     myobj["nombreArchivo"] = "nombre_de_prueba"
        #     x = requests.post(url, json = myobj)
        #     print(x)
        # return f"Data saved in the Database"

    ###### Send chunks of data instead of 1 by 1 #####

        url = 'http://localhost:5000/insertar_all_admisions'
        data = pd.DataFrame(data)
        data['nombreArchivo'] = 'nombre_de_prueba'
        data = data.to_dict('records')
        chunks = [data[x:x+10] for x in range(0, len(data), 10)]
        for i, chunk in enumerate(chunks):
            r = requests.post(url, data = json.dumps(chunk), headers = {'content-type': 'application/json'})
            assert(r.status_code == 200), f'Error, status code is: {r.status_code}'
            print(f'total processed chunk {i+1}/{len(chunks)}')

        return f"Data saved in the Database"

@callback(
        Output('output-div', 'children'),
        Output('output-div-2', 'children'),
        Input('graph-button','n_clicks'),
        State('stored-data','data'))
def make_graphs(n,data):
    if n is None:
        return dash.no_update
    else:
        daily_admisions = get_generate_df()
        adm_dummies = transform_data(daily_admisions)
        y_prob =model.predict_proba(adm_dummies) 
        y_pred = (y_prob[:,1] >= 0.25).astype(int)
        y_pred_list = y_pred.tolist()
        y_pred_dict = {'Admitted': y_pred_list.count(1), 'Not Admitted': y_pred_list.count(0)}
        df = pd.DataFrame(y_pred_dict, index=['Pred']).transpose().reset_index()
        df.rename(columns ={'index':'Status'},inplace=True)

        fig_1 = px.bar(df, x='Pred', color = 'Status')
        fig_1.update_xaxes(visible=False, showticklabels=False)
        fig_1.update_layout( yaxis_title= "Count")

        #y_pred_dict['Admitted'] / (y_pred_dict['Admitted'] + y_pred_dict['Not Admitted'])
        
        fig_2 = daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0.7,1],"yellow":[0.4,0.7],"red":[0,0.4]}},
            value=y_prob.mean().item(),
            label='Average Probability of Hospitalization',
            max=1,
            min=0,
            size = 300
        )
        return dcc.Graph(figure=fig_1), fig_2
  
@callback(
        Output('output-title', 'children'),
        Output('output-cards', 'children'),
        Input('graph-button','n_clicks'),
        State('stored-data','data')
        )
def generate_cards (n,data):
    if n is None:
        return dash.no_update
    else:
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
        return f"ER Thresholds", [dbc.Col(card) for card in cards]
        

@callback(
        Output('output-title-2', 'children'), 
        Output('output-badges', 'children'),
        Input('graph-button','n_clicks'),
        State('stored-data','data'))
def generate_bagdes(n,data):
    if n is None:
        return dash.no_update
    else:
        raw_er_admission = pd.DataFrame.from_dict(data)
        ed_bed = round(raw_er_admission['ED bed occupancy'].median(),2)
        arrival_intensity = round(raw_er_admission['Arrival intensity'].median(),2)
        las_intensity = round(raw_er_admission['LAS intensity'].median(),2)
        lwbs_intensity = round(raw_er_admission['LWBS intensity'].median(),2)

        # ER Thresholds# ##Define Thresholds con Daniel ####

        if ed_bed > 1.7:
            badge_1 = 'Danger'
        if arrival_intensity > 23:
            badge_2 = 'Warning'
        if las_intensity > 0.15:
            badge_3 = 'Approved'
        # if lwbs_intensity > 0.06:
        #     badge_4 = 'Danger'

        kpi1 = kpibadge(ed_bed, 'Average ED Bed Occupancy', badge_1)
        kpi2 = kpibadge(arrival_intensity, 'AVG Arrival within preceding hour', badge_2)
        kpi3 = kpibadge(las_intensity, 'Ambulance Arrival Intensity', badge_3)
        kpi4 = kpibadge(lwbs_intensity,'LWBS intensity', "Danger")
        badges = [  
                kpi1.display(),
                kpi2.display(),
                kpi3.display(),
                kpi4.display()
        ] 
    return f"Current Kpis", [dbc.Col(badge) for badge in badges]
      