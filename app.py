import dash
import dash_deck
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

import pydeck as pdk
import pandas as pd
import json

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

r = gerar_pydeck(total_casamentos)


app = dash.Dash(__name__)
TOOLTIP_TEXT = {"html": "{nome_municipio_destino} : {total_casamentos}"}


mapa_div = html.Div(
            dash_deck.DeckGL(
                r.to_json(), id="deck-gl", mapboxKey=MAPBOX_ACCESS_TOKEN, tooltip=TOOLTIP_TEXT, enableEvents=['click']
            ),
            style={"height": "400px", "width": "100%", "position": "relative"},
        )

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Nome do Município"),
                dcc.Dropdown(
                    id="seletor_mun",
                    options=opcoes_municipios,
                    value=3500105,
                ),
            ]
        ),
    ],
    body=True,
)


div_graficos = dbc.Card(
    [
        dcc.Graph(id="grafico_linha_hab"),
    ],
    body=True,
)


app.layout = html.Div(
    [
        mapa_div,
        controls,
        div_graficos
    
    ]
)


@app.callback(Output('seletor_mun', "value"), Input("deck-gl", 'clickInfo'))
def get_mun_name(data):
    
    if data:
        #puxa o municipio, caso tenha clicado fora já define como miss
        objeto = data.get('object') or {'destino' : 'MISS'}
        
        return objeto.get('destino', 'MISS')
    return 'MISS'
    
@app.callback(
    Output("grafico_linha_hab", "figure"), 
    Input("seletor_mun", "value"))
def update_line_chart(cod_mun):

    mask = df_municipios['cod_municipio']==cod_mun
    fig = px.line(df_municipios[mask], 
        x="Ano", y="habitantes_do_mun")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)