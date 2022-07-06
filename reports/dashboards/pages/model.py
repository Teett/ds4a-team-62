#libraries
from click import option
from dash import html , dcc, Output, Input, callback, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page
from components.data_requests.data_transformation import transform_data
from components.data_requests.get_df import get_generate_df
from models.predict_model import get_hosp_probabilities, get_hosp_pred
from visualization import visualize
import numpy as np

# dash-labs plugin call, menu name and route
register_page(__name__, path='/the-model')

################################################################################################
# Load the model and retrieve the DataFrame with today's pacients to pass to the model
################################################################################################
daily_admissions = get_generate_df()
################################################################################################
# Transform the data
################################################################################################
adm_dummies = transform_data(daily_admissions)
################################################################################################
# Run the tunned model with the selected data
################################################################################################

try:
    y_prob = get_hosp_probabilities(adm_dummies)
    y_pred = get_hosp_pred(adm_dummies)
    df = daily_admissions.copy()
    df['y_pred'] = y_pred
    df['y_prob'] = y_prob
    df['y_prob'] = df.loc[:,'y_prob'].apply(lambda x: round(x,4))
    df = df.sort_values(by = ['y_prob'])
    df["row_number"] = np.arange(len(df))

except:
    d = {'y_prob': 0}
    y_prob = pd.Series(data=d)
    y_pred = pd.Series(data=d)
    df = daily_admissions.copy()
    df['y_pred'] = y_pred
    df['y_prob'] = y_prob
    df['y_prob'] = df.loc[:,'y_prob'].apply(lambda x: round(x,4))
    df["rowname"] = df.index

print(df)

layout = html.Div(
    [
        html.H4("Choose the model to analyze:"),
        html.Br(),
        dcc.Dropdown(
                    id="ML-models",
                    options=[
                        {"label": "Stay Length", "value": "stay_length"},
                        {"label": "Admission", "value": "admission"},
                    ],
                    #multi = True
                ),
        html.Br(),
        dbc.Row(id = 'output-cards'),
        html.Br(),
        html.Br(),
        html.H4(id = 'output-title-graph'),
        html.H5(id = 'output-notes'),
        dbc.Row([
            dbc.Col(dcc.Graph(id ='output-graph'),style = {'width' : '50%'}),
            dbc.Col(dcc.Graph(id ='output-graph2'),style = {'width' : '50%'}),
            ]
        ),
        html.Br(),
        html.Div(
            [   
                dbc.Row([dbc.Col(html.H4(id = 'output-title')),
                        dbc.Col(html.H4(id='output-title2'))
                        ]
                    ),
                html.Br(),
                dbc.Row([
                        dbc.Col(id='output-image1'),
                        dbc.Col(id='output-image2')
                    ]
                ),
            ]
        )
    ], className='card'
)

@callback(
    Output('output-cards', 'children'),
    Input('ML-models','value')
)
def generate_cards(option_selected):  
    if option_selected is None:
        return no_update
    elif option_selected == 'admission':
        cards_1 = [
            dbc.Card(
                [
                    html.H2(f"73.66%", className="card-title"),
                    html.P("Model Testing Sensitivity", className="card-text"),
                ],
                body=True,
                color="light",
            ),
            dbc.Card(
                [
                    #html.H2(f"{test_acc*100:.2f}%", className="card-title"),
                    html.H2(f"65.39%", className="card-title"),
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
        return [dbc.Col(card) for card in cards_1]
    else:
        cards_2 = [
            dbc.Card(
                [
                    html.H2(f"XX.XX%", className="card-title"),
                    html.P("Model RMSE", className="card-text"),
                ],
                body=True,
                color="light",
            ),
            dbc.Card(
                [
                    #html.H2(f"{test_acc*100:.2f}%", className="card-title"),
                    html.H2(f"XX.XX%", className="card-title"),
                    html.P("Model XXXX", className="card-text"),
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
        return [dbc.Col(card) for card in cards_2]


 

@callback(
    Output('output-image1', 'children'),
    Output('output-image2', 'children'),
    Output('output-title','children'),
    Output('output-title2','children'),
    Input('ML-models','value')
)
def update_images(option_selected):
    if option_selected is None:
        return no_update
    elif option_selected == 'admission':
        image_1 = html.Img(src = 'assets/models_admission/precision_recall_threshold.png'
                        ,style={'height':'80%', 'width':'80%'}
                        ),
        image_2 = html.Img(src = 'assets/models_admission/test_confussion_matrix.png'
                        ,style={'height':'80%', 'width':'80%'}
                        ),
        return image_1, image_2, f"Precision-Recall Threshold", f"Test Confussion Matrix"
    elif option_selected == 'stay_length':
        image_3 = html.Img(src = 'assets/models_stay/Regression_1.png'
                        ,style={'height':'80%', 'width':'80%'}
                        ),
        image_4 = html.Img(src = 'assets/models_stay/Regression_2.png'
                        ,style={'height':'80%', 'width':'80%'}
                        ),
        return image_3, image_4, f"Evolution of CrossValidation in function of L1 Ratio", f"Model Coeficients"
    else:
        return no_update

@callback(
    Output('output-graph', 'figure'),
    Output('output-graph2', 'figure'),
    Output('output-title-graph', 'children'),
    Output('output-notes', 'children'),
    Input('ML-models','value')
)
def generate_log_reg(option_selected):
    if option_selected is None:
        return no_update
    elif option_selected == 'admission':
        plot_1 = visualize.logistic_regression_plot(df)
        return plot_1, plot_1, f"Logistic Regression of Patients in the ER waiting for Hospitalization", f"1: Expected Admission, 0: Might not be admitted"
    #elif option_selected == 'stay_length':
    else:
        pass
    
        
        

                
