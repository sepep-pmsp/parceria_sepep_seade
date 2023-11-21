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


df_casamentos = casamamentos()
calc_total_mun = TransformTotalMun(df_casamentos)
total_casamentos = calc_total_mun()
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

r = gerar_pydeck(total_casamentos)


app = dash.Dash(__name__)
TOOLTIP_TEXT = {"html": "{nome_municipio_destino} : {total_casamentos}"}




texto_div = html.H1('Casamentos em São Paulo',
                    className='texto_logo')
imagem_div = html.Img(src= 'https://s3-alpha-sig.figma.com/img/ecf2/8900/78198fce56ddd3802d09b086361098d1?Expires=1701648000&Signature=oggmIKbATFXl1mUJQSigtAhv0F8FrP0CK7imaSRovB1v7pQPakoy-cMT7xwKezd0VO23DCNtNKMiwCWXhbygUonhmLuOGp6RtkBzweUazt7Lcw346aKRSesZX6r7NcK9KEzD8FK92vpXH-MA3u-IZBvA7oztkGd9krsypbdm5DlZyHWTFQxnD7NwoKe4g-Sc~CAuj1aRW-Udg79cdhT1~x5VmmPWS6cVMRlwGFXqY-SHhiqmXri3xZTnkfcJkT6C~jlSXP~zwgMJwACouHZYUQGqprWbW~qM5wNaxAwihFAGn29X~~Bgyo71-EbGpKJ5dPmMWdzaLkVQuqDijbV23Q__&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4',
                      className='imagem_logo')

banner_div = html.Div([texto_div, imagem_div],
                      className='banner_div')


mapa_div = html.Div(
            dash_deck.DeckGL(
                r.to_json(), id="deck-gl", mapboxKey=MAPBOX_ACCESS_TOKEN, tooltip=TOOLTIP_TEXT, enableEvents=['click']
            ),
            style={"height": "400px", 'width': '40%', "position": "relative"},
        )



controls = dbc.Card(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="seletor_mun",
                    options=opcoes_municipios,
                    value=municipio_aleatorio
                ),

            ],            
        ),
    ],
    body=True,
)


div_graficos = dbc.Card(
    [
        dcc.Graph(id="grafico_linha_hab"),
        dcc.Graph(id="grafico_linha_nascidos_vivos"),
        dcc.Graph(id="grafico_linha_pib"),
    ],
    body=True,
)

div_graficos_selecionados = html.Div([controls, div_graficos],
                                     className='graph')

div_dashboard = html.Div([mapa_div, div_graficos_selecionados],
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
        x="Ano", y="habitantes_do_mun")
    return fig


@app.callback(
    Output("grafico_linha_nascidos_vivos", "figure"), 
    Input("seletor_mun", "value"))
def update_line_chart_nascidos_vivos(cod_mun):

    mask = df_municipios['cod_municipio']==cod_mun
    fig = px.line(df_municipios[mask], 
        x="Ano", y="Nascidos vivos")
    return fig


@app.callback(
    Output("grafico_linha_pib", "figure"), 
    Input("seletor_mun", "value"))
def update_line_chart_pib(cod_mun):

    mask = df_municipios['cod_municipio']==cod_mun
    fig = px.line(df_municipios[mask], 
        x="Ano", y="valor_do_PIB")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)