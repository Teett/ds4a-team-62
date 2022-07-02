#libraries
from dash import html , dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
from components.data_requests.data_transformation import transform_data
from components.data_requests.get_df import get_generate_df
from models.predict_model import get_hosp_probabilities, get_hosp_pred

# dash-labs plugin call, menu name and route
register_page(__name__, path='/the-model')


cards = [
    dbc.Card(
        [
            #html.H2(f"{train_acc*100:.2f}%", className="card-title"),
            html.H2(f"95.59%", className="card-title"),
            html.P("Model Testing Sensibility", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            #html.H2(f"{test_acc*100:.2f}%", className="card-title"),
            html.H2(f"80.23%", className="card-title"),
            html.P("Model Testing Specificity", className="card-text"),
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
daily_admissions = get_generate_df()
################################################################################################
# Transform the data
################################################################################################
adm_dummies = transform_data(daily_admissions)
print(adm_dummies.columns)
################################################################################################
# Run the tunned model with the selected data
################################################################################################
y_prob = get_hosp_probabilities(adm_dummies)
y_pred = get_hosp_pred(adm_dummies)

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
