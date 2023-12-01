import dash
import dash_deck
from dash import dcc, html, dash_table

import pandas as pd

from gen_mapa.mapa_arco import gerar_pydeck
from etls.scripts.casamentos import etl as casamentos
from etls.scripts.casamentos import TransformTotalMun


from config import MAPBOX_ACCESS_TOKEN


TOOLTIP_TEXT = {"html": "{nome_municipio_destino} : {total_casamentos}"}

class Map:

    def __init__(self)-> html.Div:
        self.df_casamentos = casamentos()


    def gerar_dataframe_do_componente(self)-> pd.DataFrame:
                calc_total_mun = TransformTotalMun(self.df_casamentos)
                total_casamentos = calc_total_mun()

                return total_casamentos

 
    def gerar_componente_do_mapa(self, total_casamentos:pd.DataFrame):

        r = gerar_pydeck(total_casamentos)

        
        div = html.Div(children=[
            dash_deck.DeckGL(
                r.to_json(), id="deck-gl", mapboxKey=MAPBOX_ACCESS_TOKEN, tooltip=TOOLTIP_TEXT, enableEvents=['click']
            )],
            style={"height": "400px", 'width': '100%', "position": "relative"},
        )

        return div
    
    def pipeline(self):
          
        df = self.gerar_dataframe_do_componente()
        mapa = self.gerar_componente_do_mapa(df)
        return mapa


    
    def __call__(self)-> html.Div:
        return self.pipeline()
