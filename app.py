import dash
import dash_deck
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

import pydeck as pdk
import pandas as pd
import json
import random

from etls.scripts.casamentos import etl as casamamentos
from etls.scripts.casamentos import TransformTotalMun
from etls.scripts.municipios import etl as municipios
from gen_mapa.mapa_arco import gerar_pydeck
from config import MAPBOX_ACCESS_TOKEN

from components.map import Map

app = dash.Dash(__name__)


df_municipios = municipios()


def get_opcoes_municipios(df_municipios):

    filtrado = df_municipios[['cod_municipio', 'nome_municipio']]
    renomeado = filtrado.rename({'nome_municipio' : 'label',
                                'cod_municipio' : 'value'}, axis=1)
    sem_duplicados = renomeado.drop_duplicates()

    opcoes_municipios = sem_duplicados.to_dict(orient='records')

    return opcoes_municipios

opcoes_municipios = get_opcoes_municipios(df_municipios)
municipio_aleatorio = random.choice(opcoes_municipios)['value']








texto_div = html.H1('Casamentos em São Paulo',
                    className='texto_logo')
imagem_div = html.Img(src= './assets\LOGOTIPO_PREFEITURA_HORIZONTAL_MONOCROMÁTICO_NEGATIVO.png',
                      className='imagem_logo')

banner_div = html.Div([texto_div, imagem_div],
                      className='banner_div')


mapa = Map()
mapa_div = mapa.pipeline()


controls = dbc.Card(
    [
        html.Div(
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
    body=True,
)


div_graficos = dbc.Card(
    [
        dcc.Graph(id="grafico_linha_nascidos_vivos"),
        dcc.Graph(id="grafico_linha_pib"),
    ],
)

div_grafico_e_selecao = dbc.Card([controls, dcc.Graph(id="grafico_linha_hab")
])

div_hero = html.Div([mapa_div,div_grafico_e_selecao],
                    className='map_and_graph')

div_graficos_selecionados = html.Div(div_graficos,
                                     className='graph')

div_dashboard = html.Div([div_hero, div_graficos_selecionados],
                         className='hero')


app.layout = html.Div(
    [
        banner_div,
        div_dashboard,

    ], 
    className= 'body'
)


@app.callback(Output('seletor_mun', "value"), [Input("deck-gl", 'clickInfo'), Input('seletor_mun', 'value')])
def get_mun_name(data, selecao_atual):
    
    if data:
        #puxa o municipio, caso tenha clicado fora já define como miss
        objeto = data.get('object') or {'destino' : selecao_atual}
        
        selecao = objeto.get('destino', selecao_atual)
        return selecao
    return selecao_atual


@app.callback(Output('deck-gl', 'clickInfo'), Input('seletor_mun', 'value'))
def zerar_dados_mapa(valor):

    return None

    
@app.callback(
    Output("grafico_linha_hab", "figure"), 
    Input("seletor_mun", "value"))
def update_line_chart_habitantes(cod_mun):

    mask = df_municipios['cod_municipio']==cod_mun
    fig = px.line(df_municipios[mask], 
        x="Ano", y="habitantes_do_mun", title='Habitantes do munícipio')
    fig.update_layout( template= 'plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)


    return fig


@app.callback(
    Output("grafico_linha_nascidos_vivos", "figure"), 
    Input("seletor_mun", "value"))
def update_line_chart_nascidos_vivos(cod_mun):

    mask = df_municipios['cod_municipio']==cod_mun
    fig = px.line(df_municipios[mask], 
        x="Ano", y="Nascidos vivos", title= 'Número de nascituros')
    fig.update_layout( template= 'plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)



    return fig


@app.callback(
    Output("grafico_linha_pib", "figure"), 
    Input("seletor_mun", "value"))
def update_line_chart_pib(cod_mun):

    mask = df_municipios['cod_municipio']==cod_mun
    fig = px.line(df_municipios[mask], 
        x="Ano", y="valor_do_PIB", title= 'Valor do PIB')
    fig.update_layout( template= 'plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)