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
    df["rowname"] = df.index

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
        dbc.Row(dcc.Graph(id ='output-graph')),
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
                )
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
                    html.P("Model Testing Sensitivity", className="card-text"),
                ],
                body=True,
                color="light",
            ),
            dbc.Card(
                [
                    #html.H2(f"{test_acc*100:.2f}%", className="card-title"),
                    html.H2(f"XX.XX%", className="card-title"),
                    html.P("Model Testing Specificity", className="card-text"),
                ],
                body=True,
                color="dark",
                inverse=True,
            ),
            dbc.Card(
                [
                    #html.H2(f"{dfTrain.shape[0]} / {dfTest.shape[0]}", className="card-title"),
                    html.H2(f" XXXX / XXXX", className="card-title"),
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
                        ,style={'height':'85%', 'width':'85%'}
                        ),
        image_2 = html.Img(src = 'assets/models_admission/test_confussion_matrix.png'
                        ,style={'height':'85%', 'width':'85%'}
                        ),
        return image_1, image_2, f"Precision-Recall Threshold", f"Test Confussion Matrix"
    else:
        pass

# @callback(
#     Output('output-graph', 'figure'),
#     Output('output-image1', 'children'),
#     Output('output-image2', 'children'),
#     Output('output-title','children'),
#     Output('output-title2','children'),
#     Input('ML-models','value')
# )
# def update_images(option_selected, regression_df):
#     if option_selected is None:
#         return no_update
#     elif option_selected == 'admission':
#         image_1 = html.Img(src = 'assets/models_admission/precision_recall_threshold.png'
#                         ,style={'height':'85%', 'width':'85%'}
#                         ),
#         image_2 = html.Img(src = 'assets/models_admission/test_confussion_matrix.png'
#                         ,style={'height':'85%', 'width':'85%'}
#                         ),
#         plot_1 = visualize.logistic_regression_plot(regression_df)
#         return plot_1, image_1, image_2, f"Precision-Recall Threshold", f"Test Confussion Matrix"
#     else:
#         pass
                
