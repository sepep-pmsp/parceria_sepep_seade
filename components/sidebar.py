from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

class Sidebar:
    def __init__(self):

        self.navbar =html.Div(
    [
        html.Div(
            [
                html.H2("SEPEP/SEADE", style={"color": "white"}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Dashboard")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-info-circle me-2"),
                        html.Span("Sobre"),
                    ],
                    href="/about",
                    active="exact",
                    n_clicks=0,
                    id='horizontal-collapse-button'
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-database	 me-2"),
                        html.Span("Dados"),
                    ],
                    href="/data",
                    active="exact",
                    n_clicks=0,
                    id='horizontal-collapse-button_data'
                ),
                
                dbc.NavLink(
                    [
                        html.I(className="fab fa-github me-2"),
                        html.Span("Github"),
                    ],
                    href="https://github.com/sepep-pmsp/parceria_sepep_seade",
                    target='_blank',
                    external_link=True


                    
                )
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


    def criar_componente_final(self):
        navbar_div = html.Div(self.navbar,
                                     )
        return navbar_div
        
    def pipeline(self):
        
        navbar = self.criar_componente_final()

        return navbar
    
    def __call__(self)-> html.Div:

        return self.pipeline()

