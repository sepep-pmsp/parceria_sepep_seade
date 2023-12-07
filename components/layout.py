import dash
from dash import dcc, html, dash_table

from components.map import Map
from components.banner import Banner
from components.dropdown_com_grafico import Dropdown_com_grafico
from components.outros_graficos import Outros_graficos
from components.sidebar import Sidebar
from components.footer import Footer

class Layout:

    def __init__(self):

        self.location = html.Div(dcc.Location(id="url"))

        self.sidebar = Sidebar()
        self.sidebar_div = self.sidebar()
        
        self.mapa = Map()
        self.mapa_div = self.mapa.pipeline()

        self.banner = Banner()
        self.banner_div = self.banner.pipeline()
        
        self.footer = Footer()
        self.footer_div = self.footer()

        self.dropdown_com_grafico = Dropdown_com_grafico()
        self.dropdown_com_grafico_div = self.dropdown_com_grafico.pipeline()

        self.outros_graficos = Outros_graficos()
        self.outros_graficos_div = self.outros_graficos.pipeline()

        self.mapa_grafico_e_seletor_div = html.Div([self.mapa_div, self.dropdown_com_grafico_div],
                                                   className='map_and_graph')
        self.dashboard_completo_div = html.Div([self.mapa_grafico_e_seletor_div, self.outros_graficos_div],
                                              className='hero')

    def recarregar_municipio_aleatorio(self):
        self.dropdown_com_grafico = Dropdown_com_grafico()
        self.dropdown_com_grafico_div = self.dropdown_com_grafico.pipeline()

    def servir_layout(self) -> html.Div:
        self.recarregar_municipio_aleatorio()

        layout = html.Div(
            [   self.banner_div,
             
                self.sidebar_div,

                self.location,

                html.Div([], id='page-content'),

                self.footer_div
                          
            ])

        return layout

    def pipeline(self) -> html.Div:
        layout = self.servir_layout()
        return layout

    def __call__(self) -> html.Div:
        return self.pipeline()