#libraries
import dash
from dash import Dash, html , dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
import sklearn
import pickle
import requests

# dash-labs plugin call, menu name and route
register_page(__name__, path='/the-model-test')


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

raw_er_admission = pd.read_excel('../../data/processed/admission/app_test_dataset.xlsx', sheet_name = 'Data',index_col = None)

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

#raw_er_admission = pd.read_excel('../../data/processed/admission/app_test_dataset.xlsx', sheet_name = 'Data',index_col = None)

url = 'http://localhost:5000/consulta_admision_por_nombre'
myobj["nombre"] = "nombre_de_prueba"
response = requests.post(url, json = myobj)
print(response)
print("json aja ", response.json())

response = response.json()
raw_er_admission = pd.DataFrame.from_dict(data = response['Respuesta'])
raw_er_admission.drop(['Stay_length','Admission_ALL','createdAt','currentDate','id','nombreArchivo','updatedAt'], axis = 1, inplace = True)
raw_er_admission.rename(columns = {'Inpatient_beoccupancy': 'Inpatient_bed_occupancy'}, inplace = True)

raw_er_admission = raw_er_admission.astype({"ACSC": float,
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

## Re-organize the DF adm_dummies that we are gonna pass to the model in the same order the original DF was Fitted ##

adm_dummies = adm_dummies [['DayWeek_coded','Shift_coded','Arr_Amb','Gender','Consultant_on_duty','ED bed occupancy','Inpatient_bed_occupancy',
                           'Arrival intensity', 'LAS intensity', 'LWBS intensity', 'Last_10_mins', 'Site_2.0','Site_3.0', 'Age_band_1.0',
                           'Age_band_2.0', 'Age_band_3.0', 'IMD_quintile_1.0', 'IMD_quintile_2.0', 'IMD_quintile_3.0', 'IMD_quintile_4.0',
                           'IMD_quintile_5.0','Ethnicity_2.0','Ethnicity_3.0','Ethnicity_4.0','Ethnicity_5.0','Ethnicity_6.0','ACSC_1.0', 'ACSC_3.0']]

print(adm_dummies.columns)

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
