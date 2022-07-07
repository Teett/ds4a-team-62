#libraries

from dash import html , dcc, dash_table, Input, Output, callback, State, no_update
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
from components.generate_names import generate_name
from components.data_requests.get_df import get_generate_df
from components.data_requests.data_transformation import transform_data, reg_transform_data
import pickle
import dash_daq as daq
from visualization import visualize
from models.predict_model import get_hosp_probabilities, get_hosp_pred, get_reg_prediction


# dash-labs plugin call, menu name and route
register_page(__name__, path='/')

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

#Load the model to showw results in Insights:

with open('../../models/admission/model_1_elastic_net_tunned.pickle', 'rb') as f:
    model = pickle.load(f)

## Load Cards to set up the Emergency Room Thresholds based on historic data:

raw_er_admission = pd.read_excel('../../data/raw/er_admission.xlsx', sheet_name = 'Data')
bed_occupancy = raw_er_admission['Inpatient_bed_occupancy'].mean()
arrival_intensity = raw_er_admission['Arrival intensity'].mean()
las_intensity = raw_er_admission['LAS intensity'].mean()
lwbs_intensity = raw_er_admission['LWBS intensity'].mean()
stay_length = raw_er_admission['Stay_length'].mean()

cards = [
dbc.Card(
    [
        html.H2(f"{bed_occupancy*100:.2f}%", className="card-title"),
        html.P("AVG Bed Occupancy", className="card-text"),
    ],
    body=True,
    color="light",
),
dbc.Card(
    [
        html.H2(f"{arrival_intensity:.2f}", className="card-title"),
        html.P("AVG Arrivals within the preceding hour", className="card-text"),
    ],
    body=True,
    color="dark",
    inverse=True,
),
dbc.Card(
    [
        html.H2(f"{las_intensity*100:.2f}%", className="card-title"),
        html.P("AVG Arrivals by Ambulance", className="card-text"),
    ],
    body=True,
    color="primary",
    inverse=True,
),
dbc.Card(
    [
        html.H2(f"{lwbs_intensity*100:.2f}%", className="card-title"),
        html.P("Patients within the hour who leave without being seen by a Doctor", className="card-text",style={'textAlign': 'center'}),
    ],
    body=True,
    color="light",
),
]

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
        html.H4("ER Thresholds"),
        html.Br(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        html.Div([
            html.H4(id= "output-title-2"),
            html.Br(),
            dbc.Row(id ='output-badges'),
            html.Br(),
            html.H4(id= 'output-title-3'),
            html.Br(),
            dbc.Row([
                dbc.Col(id='output-div',   style = {'width': '50%'}),
                dbc.Col(id='output-div-2', style = {'width': '25%'}),
                dbc.Col(id='output-div-3', style = {'width': '25%'})
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(id='output-table', style = {'width':'50%'})
                    ]
                ),
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
            html.H4('This is a preview of the file you are about to upload'),#, style= "color: navy"),
            html.H5('Note: If want to include this data in the Calculated Insights for Today, please firt save the file in the DataBase'),
            html.H5(f"File uploaded: {filename}"),
            html.H6(f"Date:{datetime.datetime.fromtimestamp(date)}"),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=5
            ),
            dcc.Store(id='stored-data', data=df.to_dict('records')),
            html.Hr(),
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
    if n is None:
        return no_update
    else:
        url = 'http://localhost:5000/insertar_all_admisions'
        data = pd.DataFrame(data)
        data['nombreArchivo'] = 'nombre_de_prueba'
        data = data.to_dict('records')
        chunks = [data[x:x+100] for x in range(0, len(data), 100)]
        for i, chunk in enumerate(chunks):
            r = requests.post(url, data = json.dumps(chunk), headers = {'content-type': 'application/json'})
            assert(r.status_code == 200), f'Error, status code is: {r.status_code}'
            print(f'total processed chunk {i+1}/{len(chunks)}')
        return f"Data saved in the Database"

@callback(
        Output('output-div', 'children'),
        Output('output-div-2', 'children'),
        Output('output-div-3', 'children'),
        Output('output-table', 'children'),
        Output('output-title-3', 'children'),
        Input('graph-button','n_clicks'),
        )
def make_graphs(n):
    if n is None:
        return no_update
    else:
        ## Predictions of Hospitalization:
        daily_admissions = get_generate_df()
        adm_dummies = transform_data(daily_admissions)
        y_prob_list = get_hosp_probabilities(adm_dummies)
        y_pred = get_hosp_pred(adm_dummies)
        gauge_value = sum(y_prob_list)/len(y_prob_list)
        
        df_fig = daily_admissions.copy()
        fig_1 = visualize.admissions_plot(y_pred,df_fig)
        
        fig_2 = daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0.35,0.50],"yellow":[0.20,0.35],"red":[0,0.2]}},
            value= gauge_value,
            label='Average Probability of Hospitalization',
            max=0.5,
            min=0,
            size = 300
        )

        ## Predictions of the regression for time spent in the ER:

        df_regression = get_generate_df()
        df_regression["Admission_ALL"] = y_pred
        reg_dummies = reg_transform_data(df_regression)
        y_pred_reg = get_reg_prediction(reg_dummies)
        df_regression['Stay_length'] = y_pred_reg

        fig_3 = daq.Gauge(
            color={"gradient":True,"ranges":{"green":[0,75],"yellow":[75,120],"red":[120,200]}},
            value=y_pred_reg.mean().item(),
            label='Average time in Emergency Dept.',
            max=200,
            min=0,
            size = 300
        )
        
        ## Creating the final DF with all predictions results: 

        df = daily_admissions.copy()
        #df['Expected_ER_stay'] =  waiting for regression model
        df['Status'] = y_pred
        df['Hosp_prob'] = y_prob_list
        df['Hosp_prob'] = df.loc[:,'Hosp_prob'].apply(lambda x: round(x,4))
        df['Stay_length'] = y_pred_reg
        df["Name"] = df.apply(lambda x: generate_name(), axis=1)
        ## Now Creating df for the table that will be displayed:

        df_table = df[['Name','Site','Age_band','Gender','Status','Hosp_prob','Stay_length']]
        dict_admissions = {1: 'Expected Admission', 0: 'Might Not be Admitted'}
        dict_gen = {0: 'male', 1: 'female'}
        dict_age = {0: '16-34',
                1: '35-64',
                2: '65-84',
                3: '85 and over'}
        df_table.replace({'Gender': dict_gen,
                    'Status': dict_admissions,
                    'Age_band': dict_age}, inplace = True)
        table = dash_table.DataTable(
                data=df_table.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df_table.columns],
                page_size=12
            ),
        
        ## Histogram ##

        return dcc.Graph(figure=fig_1), fig_2, fig_3, table, f"Expected Predictions"

@callback(
        Output('output-title-2', 'children'), 
        Output('output-badges', 'children'),
        Input('graph-button','n_clicks')
        )
def generate_bagdes(n):
    if n is None:
        return no_update
    else:
        er_admission = get_generate_df()
        ed_bed = round(er_admission['Inpatient_bed_occupancy'].mean(),2)
        arrival_intensity = round(er_admission['Arrival intensity'].mean(),2)
        las_intensity = round(er_admission['LAS intensity'].mean(),2)
        lwbs_intensity = round(er_admission['LWBS intensity'].mean(),2)

        # Using ER Thresholds for Bagdes Kpis later on: ##

        # Badge 1:
        if  ed_bed >= 0.90:
            badge_1 = 'Danger'
        elif ed_bed >= 0.80 and ed_bed < 0.90:
            badge_1 = 'Warning'
        else:
            bagde_1 = 'Normal'
        # Badge 2:
        if arrival_intensity >= 20:
            badge_2 = 'Danger' 
        elif arrival_intensity >= 15 and arrival_intensity <20:
            badge_2 = 'Warning'
        else:
            badge_2 = 'Normal' 
        # Badge 3:
        if las_intensity >= 0.50:
            badge_3 = 'Danger'
        if las_intensity >= 0.30 and las_intensity < 0.50:
            badge_3 = 'Warning'
        else:
            badge_3 = 'Normal'
        # Badge 4:
        if lwbs_intensity >= 0.15:
            badge_4 = 'Danger'
        elif lwbs_intensity >= 0.7 and lwbs_intensity < 0.15:
            badge_4 = 'Warning'
        else:
            badge_4 = 'Normal'
        
        kpi1 = kpibadge(f"{ed_bed*100:.2f}%", 'AVG Bed Occupancy', badge_1)
        kpi2 = kpibadge(f"{arrival_intensity:.2f}", 'AVG Arrivals within the preceding hour', badge_2)
        kpi3 = kpibadge(f"{las_intensity*100:.2f}%", 'AVG Arrivals by Ambulance', badge_3)
        kpi4 = kpibadge(f"{lwbs_intensity*100:.2f}%",'Patients within the hour who leave without being seen by a Doctor', badge_4)
        badges = [  
                kpi1.display(),
                kpi2.display(),
                kpi3.display(),
                kpi4.display()
        ] 
    return f"Current Kpis", [dbc.Col(badge) for badge in badges]