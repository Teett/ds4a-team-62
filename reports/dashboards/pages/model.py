#libraries
import dash
from dash import Dash, html , dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
import sklearn
import pickle

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

raw_er_admission = pd.read_excel('../../data/processed/admission/app_test_dataset.xlsx', sheet_name = 'Data',
                                index_col = None)

raw_er_admission = raw_er_admission.astype({"ACSC": float,
                                            "Age_band": float,
                                            "Ethnicity": float,
                                            "Site": float,
                                            "IMD_quintile": float})

################################################################################################
# Load the model
################################################################################################
with open('../../models/admission/model_1_elastic_net_tunned.pickle', 'rb') as f:
    model = pickle.load(f)

################################################################################################
# Transform the data
################################################################################################
# %% analyize missingess
# impute 3, this new category will mean that there it is not know if the patient has a sensitive condition
er_admission = raw_er_admission.copy()
er_admission['ACSC'] = raw_er_admission['ACSC'].fillna(3)
# impute category 5 (unknown) to the ethnicity variable
er_admission['Ethnicity'] = raw_er_admission['Ethnicity'].fillna(5)
# drop the other null values, only 24 records will be discarded
er_admission = er_admission.dropna()
# get dummies
adm_dummies = pd.get_dummies(er_admission, 
                            columns=['Site','Age_band','IMD_quintile','Ethnicity', 'ACSC'], 
                            drop_first=True)
#adm_dummies = adm_dummies.drop(['Admission_ALL', 'Stay_length'], axis = 1)

# %%
################################################################################################
# Run the tunned model with the selected data
################################################################################################
y_prob =model.predict_proba(adm_dummies) 
y_pred = (y_prob[:,1] >= 0.25).astype(int)

print(y_pred)


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
