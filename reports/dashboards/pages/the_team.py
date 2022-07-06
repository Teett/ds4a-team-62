#libraries
import dash
from dash import Dash, html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page


# dash-labs plugin call, menu name and route
register_page(__name__, path='/the-team')

# specific layout for this page

##Images paths ##

image_path = 'assets/DS4A.png'
team_image_path = 'assets/DS4A Team 62.png'
daniel = 'assets/Daniel.png'
maria = 'assets/Maria.png'
jeyson = 'assets/Jeyson.png'
juan = 'assets/Juan.png'
luis = 'assets/foto team.png'
cristian = 'assets/Cristian.png' 

layout = html.Div(
    [   
    dbc.Row(html.Img(src = team_image_path,style={'height':'30%', 'width':'30%','display': 'block','margin-left': 'auto','margin-right': 'auto'})),
    html.Hr(),
    dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Luis Felipe Serna"),
                        html.Br(),
                        html.Img(src = luis,style={'height':'60%', 'width':'60%'})
                    ]   
                        ),
                dbc.Col(
                    [
                        html.H5("Luis Daniel Chavarria"),
                        html.Br(),
                        html.Img(src = daniel,style={'height':'60%', 'width':'60%'})
                    ]   
                        ),
                dbc.Col(
                    [
                        html.H5("Maria Paula Alvarez"),
                        html.Br(),
                        html.Img(src = maria,style={'height':'60%', 'width':'60%'})
                    ]   
                        ),
                dbc.Col(
                    [
                        html.H5("Juan Barrios"),
                        html.Br(),
                        html.Img(src = juan,style={'height':'60%', 'width':'60%'})
                    ]   
                        ),                    
                dbc.Col(
                    [
                        html.H5("Jeyson Guzman"),
                        html.Br(),
                        html.Img(src = jeyson,style={'height':'60%', 'width':'60%'})
                    ]
                        ),
                dbc.Col(
                    [
                        html.H5("Cristian Rodriguez"),
                        html.Br(),
                        html.Img(src = cristian,style={'height':'60%', 'width':'60%'})
                    ]
                        ), 
            ]
        )  
    ]
)