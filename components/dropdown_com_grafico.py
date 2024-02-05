from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from etls.scripts.municipios import etl as municipios
import random





class Dropdown_com_grafico:
    def __init__(self):

        self.df_municipios = municipios()
        self.fig = dict(layout=dict(template ='plotly_dark', plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono" ))

    def receber_opcoes_municipios(self):

        filtrado = self.df_municipios[['cod_municipio', 'nome_municipio']]
        renomeado = filtrado.rename({'nome_municipio' : 'label',
                                    'cod_municipio' : 'value'}, axis=1)
        sem_duplicados = renomeado.drop_duplicates()

        opcoes_municipios = sem_duplicados.to_dict(orient='records')

        return opcoes_municipios
    
    def receber_municipio_aleatorio(self):
        opcoes_municipios = self.receber_opcoes_municipios()
        municipio_aleatorio = random.choice(opcoes_municipios)['value']

        return municipio_aleatorio
        

    def criar_componente_final(self, opcoes_municipios, municipio_aleatorio):
        controle_div = dbc.Container(
            [
                dbc.Container(
                    [
                        dcc.Dropdown(
                            id="seletor_mun",
                            options=opcoes_municipios,
                            value=municipio_aleatorio,
                            className='dropdown'
                        ),
                    ],                        
                ),
            ],
            id='dropdown')
        
        grafico_e_controle_div = dbc.Container([controle_div, dcc.Graph(id="grafico_linha_hab", figure=self.fig)])

        return grafico_e_controle_div

        
        
    def pipeline(self):

        opcoes_municipios = self.receber_opcoes_municipios()
        municipio_aleatorio = self.receber_municipio_aleatorio()
        grafico_e_controle_div = self.criar_componente_final(opcoes_municipios,municipio_aleatorio)

        return grafico_e_controle_div
      
    
    def __call__(self)-> html.Div:

        return self.pipeline()
