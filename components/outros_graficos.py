from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
 
 
 
class Outros_graficos:
    def __init__(self):
       
       
        self.fig = dict(layout=dict(template ='plotly_dark', plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono" ))
        self.outros_graficos_card = html.Div([dcc.Graph(id="grafico_linha_nascidos_vivos", className='nasc_graph', figure=self.fig), dcc.Graph(id="grafico_linha_pib", className='pib_graph', figure=self.fig)])
       
 
    def criar_componente_final(self):
        outros_graficos_div = html.Div([self.outros_graficos_card],
                                     className='graph')
        return outros_graficos_div
       
    def pipeline(self):
       
        outros_graficos = self.criar_componente_final()
 
        return outros_graficos
   
    def __call__(self)-> html.Div:
 
        return self.pipeline()