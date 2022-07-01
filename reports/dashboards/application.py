import dash
import dash_bootstrap_components as dbc
from dash import html
import dash_labs as dl

app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY],)

#Top menu, items get from all pages registered with plugin.pages

navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink( "Dashboard", href='/')),
    dbc.NavItem(dbc.NavLink( "Descriptive Analytics", href="/analytics")),
    dbc.NavItem(dbc.NavLink( "The Model", href="/the-model")),
    dbc.NavItem(dbc.NavLink("The Team", href="/the-team")),
    ],
    brand="DS4A Project - Team 62",
    color="primary",
    dark=True,
    className="mb-2",
)

### Layout####
app.layout = html.Div(
    [
    dbc.Row(
            [
                html.H1('CLINICAL OUTCOME RISK ASSESTMENT TOOL',style={'textAlign': 'center'}),
                html.Hr()
                ],
            className = 'title'
            ),
    dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
    ],
    className="dbc",
    fluid=True,
    ),
    ]
)

if __name__ == "__main__":
    app.run_server(port=8888)