import dash
import dash_deck
import dash_html_components as html
import pydeck as pdk
import pandas as pd


from etls.scripts.casamentos import etl as casamamentos
from etls.scripts.municipios import etl as municipios
from dash_exemplo.mapa_arco import gerar_pydeck




df_casamentos = casamamentos()
df_municipios = municipios()


r = gerar_pydeck(df_casamentos.fillna(0))





app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(), id="deck-gl"
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)