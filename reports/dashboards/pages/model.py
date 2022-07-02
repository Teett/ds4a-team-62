#libraries
from dash import html , dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
import pickle
from components.data_requests.get_df import get_generate_df
from components.data_requests.data_transformation import transform_data

# dash-labs plugin call, menu name and route
register_page(__name__, path='/the-model')


cards = [
    dbc.Card(
        [
            #html.H2(f"{train_acc*100:.2f}%", className="card-title"),
            html.H2(f"95.59%", className="card-title"),
            html.P("Model Training Accuracy", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            #html.H2(f"{test_acc*100:.2f}%", className="card-title"),
            html.H2(f"80.23%", className="card-title"),
            html.P("Model Test Accuracy", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            #html.H2(f"{dfTrain.shape[0]} / {dfTest.shape[0]}", className="card-title"),
            html.H2(f" 13.529 / 6.208", className="card-title"),
            html.P("Train / Test Split", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
]

################################################################################################
# Load the model and retrieve the DataFrame with today's pacients to pass to the model
################################################################################################

with open('../../models/admission/model_1_elastic_net_tunned.pickle', 'rb') as f:
    model = pickle.load(f)
daily_admissions = get_generate_df()

################################################################################################
# Transform the data
################################################################################################

adm_dummies = transform_data(daily_admissions)
print(adm_dummies.columns)

################################################################################################
# Run the tunned model with the selected data
################################################################################################
try:
    y_prob =model.predict_proba(adm_dummies) 
    y_pred = (y_prob[:,1] >= 0.25).astype(int)
except:
    d = {'y_prob': 0}
    y_prob = pd.Series(data=d)
    y_pred = pd.Series(data=d)
print(list(y_pred))
print(type(y_pred))
print(y_prob)
print(y_prob.mean())
print(type(y_prob.mean().item())) #.item() is to convert the numpy.float64 data type to a python native float type


layout = html.Div(
    [
        html.P("Choose the model to analyze:"),
        html.Hr(),
        dcc.Dropdown(
                    id="ML-models",
                    options=[
                        {"label": "Stay Length", "value": "stay_length"},
                        {"label": "Admission", "value": "admission"},
                    ],
                    value=['stay_length_regression', 'admission_classification'],
                    #multi = True
                ),
        html.Br(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
        dcc.Graph(id="heatmaps-graph"),
        
    ], className='card'
)
