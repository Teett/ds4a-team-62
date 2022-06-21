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

layout = dbc.Container(
    [
        #dbc.Row(html.H1(['The Team'],id="div_title_team")), 
        html.Div(
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
                                        ]   
                                            ),
                                    dbc.Col(
                                        [
                                            html.Div("Luis Daniel Chavarria"),
                                            html.Br(),
                                            html.Img(src = daniel,style={'height':'60%', 'width':'60%'})
                                        ]   
                                            ),
                                    dbc.Col(
                                        [
                                            html.Div("Maria Paula Alvarez"),
                                            html.Br(),
                                            html.Img(src = maria,style={'height':'60%', 'width':'60%'})
                                        ]   
                                            ),
                                    dbc.Col(
                                        [
                                            html.Div("Juan Barrios"),
                                            html.Br(),
                                            html.Img(src = juan,style={'height':'60%', 'width':'60%'})
                                        ]   
                                            ),                    
                                    dbc.Col(
                                        [
                                            html.Div("Jeyson Guzman"),
                                            html.Br(),
                                            html.Img(src = jeyson,style={'height':'60%', 'width':'60%'})
                                        ]
                                            ),
                                    dbc.Col(
                                        [
                                            html.Div("Cristian Rodriguez"),
                                            html.Br(),
                                            html.Img(src = cristian,style={'height':'60%', 'width':'60%'})
                                        ]
                                            ), 
                                ]
                            )  
                        ]
                )

    ]
)