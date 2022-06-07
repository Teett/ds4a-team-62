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
import plotly.express as px
import pandas as pd
import json
import os

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


sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
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

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div(
    [
    dcc.Location(id="url"),
    html.Div(
        [
            dbc.Row(
                [
                    html.H1('CLINICAL OUTCOME RISK ASSESTMENT TOOL')
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
                dbc.Row("Luis Serna"),
                dbc.Row("Jeyson Guzman"),
                dbc.Row("Cristian Rodriguez"),
                dbc.Row("Juan Barrios"),
                dbc.Row("Luis Daniel Chavarria"),
                dbc.Row("Maria Paula Alvarez"),
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