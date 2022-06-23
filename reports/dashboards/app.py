import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, dash_table
import pandas as pd
import plotly.express as px
import dash_labs as dl


app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY],)
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# the style arguments for the sidebar. We use position:fixed and a fixed width

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 130,
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

df = pd.read_csv('../../data/raw/superstore.csv', parse_dates=['Order Date', 'Ship Date'])
raw_er_admission = pd.read_excel('../../data/raw/er_admission.xlsx', sheet_name = 'Data')

##Create ScatterPlot of variable correlations:

#corr_variables = visualize.correlation_plot(raw_er_admission)

correlations = raw_er_admission.corr()
corr_variables = px.imshow(correlations, text_auto = True, aspect = 'auto')

corr_variables.update_layout(
    title="Variables Correlation"
)

##Histogram for admitted and stay length

graph_hist = raw_er_admission.loc[:,['Stay_length','Gender']]
graph_hist['Gender'] = graph_hist['Gender'].apply(lambda x: "Female" if(x == 1) else "Male")
graph_hist
 
hist_fig = px.histogram(graph_hist, x="Stay_length", color="Gender")

##DataTable to change later (its just an example of a table)

table_df = raw_er_admission.loc[:,['Gender','Age_band','Stay_length','Admission_ALL']].head()

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

#Top menu, items get from all pages registered with plugin.pages

navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink( "Home", href='/')),
    dbc.NavItem(dbc.NavLink( "Dashboard", href='/dashboard')),
    dbc.NavItem(dbc.NavLink( "The Model", href="/the-model")),
    dbc.DropdownMenu(
        [

            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Descriptive Analytics",
    ),
    dbc.NavItem(dbc.NavLink("The Team", href="/the-team")),
    ],
    brand="DS4A Project - Team 62",
    color="primary",
    dark=True,
    className="mb-2",
)

##Sidebar ##

# sidebar = html.Div(
#     [
#         #html.H2("Sidebar", className="display-4"),
#         html.Img(src = image_path,style={'height':'23%', 'width':'82%'}),
#         html.Hr(),
#         html.P(
#             "A simple sidebar layout with navigation links", className="lead"
#         ),
#         dbc.Nav(
#             [
#                 dbc.NavLink("Dashboard", href="/", active="exact"),
#                 dbc.NavLink("The Model", href="/page-1", active="exact"),
#                 dbc.NavLink("Descriptive analytics", href="/page-2", active="exact"),
#                 dbc.NavLink("The Team", href="/page-3", active="exact"),
#             ],
#             vertical=True,
#             pills=True,
#         ),
#     ],
#     style=SIDEBAR_STYLE,
# )

## Content###

content = html.Div(id="page-content", style=CONTENT_STYLE)

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

# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])

# def render_page_content(pathname):
#     if pathname == "/":
#         return html.Div([
#             dbc.Row([
#                 dbc.Col("Key Variable Inputs",md=6),
#                 dbc.Col("Model Output", md=6)
#             ]),
#             html.Br(),
#             dbc.Row([
#                 dbc.Col([
#                     dbc.Row(dcc.Dropdown(id='my_first_drop', placeholder = 'first_drop',
#                                 options =[{'label':'Option A','value':'Optiona A'},
#                                           {'label': 'Option B', 'value': 'Option B'}])),
#                     dbc.Row(dcc.Dropdown(id='my_first_drop', placeholder = 'first_drop',
#                                 options =[{'label':'Option A','value':'Optiona A'},
#                                           {'label': 'Option B', 'value': 'Option B'}])),
#                     dbc.Row(dcc.Dropdown(id='my_first_drop', placeholder = 'first_drop',
#                                 options =[{'label':'Option A','value':'Optiona A'},
#                                           {'label': 'Option B', 'value': 'Option B'}])),
#                     html.Br(),
#                     dbc.Row(dash_table.DataTable(table_df.to_dict('records'), [{"name": i, "id": i} for i in table_df.columns]))                                                                                                                      
#                                           ],md=6),
#                 dbc.Col( dcc.Graph(figure=Treemap_fig, id="Treemap"), md=6)
#             ]),
#             html.Br(),
            
#         ]
#                     )
#     elif pathname == "/page-1":
#         return html.Div([

#             dbc.Row([dbc.Col(card) for card in cards]),
#             html.Br(),
#             dbc.Row([
#                 dbc.Col("Key Variable Inputs",md=6),
#                 dbc.Col("Model Output", md=6)
#             ]),
#             dbc.Row([
#                 dbc.Col(dcc.Dropdown(id='my_first_drop', placeholder = 'first_drop',
#                                 options =[{'label':'Option A','value':'Optiona A'},
#                                           {'label': 'Option B', 'value': 'Option B'}]),md=6),
#                 dbc.Col( dcc.Graph(figure=Treemap_fig, id="Treemap"), md=6)
#             ]),
#         ]
#                     )
#     elif pathname == "/page-2":
#          return html.Div([
#             dbc.Row([
#                 dbc.Col(dbc.Col(dcc.Graph(figure=Scatter_fig, id="Scatter")),md=6),
#                 dbc.Col(dbc.Col(dcc.Graph(figure=corr_variables, id="Correlation")),md=6)
#             ]),
#             dbc.Row([
#                 dbc.Col(dbc.Col(dcc.Graph(figure=hist_fig)),md=6),
#                 dbc.Col(dcc.Graph(figure=Treemap_fig, id="Treemap"), md=6)
#             ]),
#         ]
#                     )
#     elif pathname == "/page-3":
#         return html.Div(
#             [   
#                 dbc.Row(html.Img(src = team_image_path,style={'height':'50%', 'width':'30%','display': 'block','margin-left': 'auto','margin-right': 'auto'})),
#                 html.Hr(),
#                 dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                         html.Div("Luis Felipe Serna"),
#                         html.Br(),
#                         html.Img(src = luis,style={'height':'60%', 'width':'60%'})
#                             ]),
#                     dbc.Col(
#                         [
#                         html.Div("Luis Daniel Chavarria"),
#                         html.Br(),
#                         html.Img(src = daniel,style={'height':'60%', 'width':'60%'})
#                             ]),
#                     dbc.Col(
#                         [
#                         html.Div("Maria Paula Alvarez"),
#                         html.Br(),
#                         html.Img(src = maria,style={'height':'60%', 'width':'60%'})
#                             ]),
#                     dbc.Col(
#                         [
#                         html.Div("Juan Barrios"),
#                         html.Br(),
#                         html.Img(src = juan,style={'height':'60%', 'width':'60%'})
#                             ]),                    
#                     dbc.Col(
#                         [
#                         html.Div("Jeyson Guzman"),
#                         html.Br(),
#                         html.Img(src = jeyson,style={'height':'60%', 'width':'60%'})
#                             ]),
#                     dbc.Col(
#                         [
#                         html.Div("Cristian Rodriguez"),
#                         html.Br(),
#                         html.Img(src = cristian,style={'height':'60%', 'width':'60%'})
#                             ]), 
#                         ]
#                       )  
#                     ]
#                 )
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )

if __name__ == "__main__":
    app.run_server(port=8888)