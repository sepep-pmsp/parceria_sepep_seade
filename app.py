import dash
import dash_deck
import dash_html_components as html
from dash.dependencies import Input, Output

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


r = gerar_pydeck(total_casamentos)


app = dash.Dash(__name__)
TOOLTIP_TEXT = {"html": "{nome_municipio_destino} : {total_casamentos}"}

app.layout = html.Div(
    [
        html.Div(
            dash_deck.DeckGL(
                r.to_json(), id="deck-gl", mapboxKey=MAPBOX_ACCESS_TOKEN, tooltip=TOOLTIP_TEXT, enableEvents=['click']
            ),
            style={"height": "400px", "width": "100%", "position": "relative"},
        ),
        html.Div(
            html.Pre(
                id='output_data'
            )
        )
    ]
)


@app.callback(Output('output_data', "children"), Input("deck-gl", 'clickInfo'))
def dump_json(data):
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    app.run_server(debug=True)