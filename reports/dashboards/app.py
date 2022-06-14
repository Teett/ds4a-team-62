"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

################################################################################################
# Load the data and create the map
################################################################################################

df = pd.read_csv('data/raw/superstore.csv', parse_dates=['Order Date', 'Ship Date'])
raw_er_admission = pd.read_excel('data/raw/er_admission.xlsx', sheet_name = 'Data')

## Create the TreeMap

Treemap_fig = px.treemap(
    df,
    path=["Category", "Sub-Category", "State"],
    values="Sales",
    color_discrete_sequence=px.colors.qualitative.Dark24,
)

#Create the Scatter_fig
Scatter_fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["State", "Sub-Category", "Order ID", "Product Name"],
)
Scatter_fig.update_layout(
    title="Sales vs. Profit in selected states", paper_bgcolor="#F8F9F9"
)

##Images paths ##

image_path = 'assets/DS4A.png'
team_image_path = 'assets/DS4A Team 62.png'
daniel = 'assets/Daniel.png'
maria = 'assets/Maria.png'
jeyson = 'assets/Jeyson.png'
juan = 'assets/Juan.png'
luis = 'assets/foto team.png'
#cristian = pending

##Sidebar ##

sidebar = html.Div(
    [
        #html.H2("Sidebar", className="display-4"),
        html.Img(src = image_path,style={'height':'23%', 'width':'82%'}),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/", active="exact"),
                dbc.NavLink("The Model", href="/page-1", active="exact"),
                dbc.NavLink("Descriptive analytics", href="/page-2", active="exact"),
                dbc.NavLink("The Team", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

## Content###

content = html.Div(id="page-content", style=CONTENT_STYLE)

## Card components ##

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

### Layout####
app.layout = html.Div(
    [
    dcc.Location(id="url"),
    html.Div(
        [
            dbc.Row(
                [
                    html.H1('CLINICAL OUTCOME RISK ASSESTMENT TOOL',style={'textAlign': 'center'}),
                    html.Hr()
                    ]
                )
        ]),
    dbc.Col(sidebar),
    dbc.Col(content)
    ]
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            dbc.Row([
                dbc.Col("Key Variable Inputs",md=4),
                dbc.Col("Model Output", md=8)
            ]),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='my_first_drop', placeholder = 'first_drop',
                                options =[{'label':'Option A','value':'Optiona A'},
                                          {'label': 'Option B', 'value': 'Option B'}]),md=4),
                dbc.Col( dcc.Graph(figure=Treemap_fig, id="Treemap"), md=8)
            ]),
        ]
                    )
    elif pathname == "/page-1":
        return html.Div([

            dbc.Row([dbc.Col(card) for card in cards]),
            html.Br(),
            dbc.Row([
                dbc.Col("Key Variable Inputs",md=6),
                dbc.Col("Model Output", md=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='my_first_drop', placeholder = 'first_drop',
                                options =[{'label':'Option A','value':'Optiona A'},
                                          {'label': 'Option B', 'value': 'Option B'}]),md=6),
                dbc.Col( dcc.Graph(figure=Treemap_fig, id="Treemap"), md=6)
            ]),
        ]
                    )
    elif pathname == "/page-2":
         return html.Div([
            dbc.Row([
                dbc.Col(dbc.Col(dcc.Graph(figure=Scatter_fig, id="Scatter")),md=6),
                dbc.Col("Model Output", md=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='my_first_drop', placeholder = 'first_drop',
                                options =[{'label':'Option A','value':'Optiona A'},
                                          {'label': 'Option B', 'value': 'Option B'}]),md=6),
                dbc.Col(dcc.Graph(figure=Treemap_fig, id="Treemap"), md=6)
            ]),
        ]
                    )
    elif pathname == "/page-3":
        return html.Div(
            [   
                dbc.Row(html.Img(src = team_image_path,style={'height':'50%', 'width':'30%','display': 'block','margin-left': 'auto','margin-right': 'auto'})),
                html.Hr(),
                dbc.Row(
                [
                    dbc.Col(
                        [
                        html.Div("Luis Felipe Serna"),
                        html.Br(),
                        html.Img(src = luis,style={'height':'60%', 'width':'60%'})
                            ]),
                    dbc.Col(
                        [
                        html.Div("Luis Daniel Chavarria"),
                        html.Br(),
                        html.Img(src = daniel,style={'height':'60%', 'width':'60%'})
                            ]),
                    dbc.Col(
                        [
                        html.Div("Maria Paula Alvarez"),
                        html.Br(),
                        html.Img(src = maria,style={'height':'60%', 'width':'60%'})
                            ]),
                    dbc.Col(
                        [
                        html.Div("Juan Barrios"),
                        html.Br(),
                        html.Img(src = juan,style={'height':'60%', 'width':'60%'})
                            ]),                    
                    dbc.Col(
                        [
                        html.Div("Jeyson Guzman"),
                        html.Br(),
                        html.Img(src = jeyson,style={'height':'60%', 'width':'60%'})
                            ]),
                    dbc.Col(
                        [
                        html.Div("Cristian Rodriguez"),
                        html.Br(),
                        #html.Img(src = daniel,style={'height':'60%', 'width':'10%'})
                            ]), 
                        ]
                      )  
                    ]
                )
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(port=8888)