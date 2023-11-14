import dash
import dash_deck
import dash_html_components as html
import pydeck as pdk
import pandas as pd


from etls.scripts.casamentos import etl as casamamentos
from etls.scripts.casamentos import TransformTotalMun
from etls.scripts.municipios import etl as municipios
from dash_exemplo.mapa_arco import gerar_pydeck
from config import MAPBOX_ACCESS_TOKEN


df_casamentos = casamamentos()
calc_total_mun = TransformTotalMun(df_casamentos)
total_casamentos = calc_total_mun()
df_municipios = municipios()


r = gerar_pydeck(total_casamentos)


app = dash.Dash(__name__)
TOOLTIP_TEXT = {"html": "{nome_municipio_destino} : {total_casamentos}"}

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(), id="deck-gl", mapboxKey=MAPBOX_ACCESS_TOKEN, tooltip=TOOLTIP_TEXT
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)