#libraries
import dash
from dash import Dash, html , dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash_labs.plugins import register_page

# dash-labs plugin call, menu name and route
register_page(__name__, path='/dashboard')

# from components.kpi.kpibadge import kpibadge

# kpi1 = kpibadge('325', 'Total kpi')
# kpi2 = kpibadge('1500', 'Total sales')
# kpi3 = kpibadge('325', 'Total transacciones')
# kpi4 = kpibadge('2122','Total User')


raw_er_admission = pd.read_excel('../../data/raw/er_admission.xlsx', sheet_name = 'Data')

ed_bed = raw_er_admission['ED bed occupancy'].mean()
arrival_intensity = raw_er_admission['Arrival intensity'].mean()
las_intensity = raw_er_admission['LAS intensity'].mean()
lwbs_intensity = raw_er_admission['LWBS intensity'].mean()

cards = [
    dbc.Card(
        [
            html.H2(f"{ed_bed:.2f}", className="card-title"),
            html.P("Average ED Bed Occupancy", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H2(f"{arrival_intensity:.2f}", className="card-title"),
            html.P("AVG Arrival within preceding hour", className="card-text"),
        ],
        body=True,
        color="dark",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2(f"{las_intensity:.2f}", className="card-title"),
            html.P("Ambulance Arrival Intensity", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2(f"{lwbs_intensity:.2f}", className="card-title"),
            html.P("LWBS intensity", className="card-text"),
        ],
        body=True,
        color="light",
    ),
]

layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Br(),
    ]
)