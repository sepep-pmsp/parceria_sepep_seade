import streamlit as st
from etls.scripts.casamentos import etl as casamamentos
from etls.scripts.municipios import etl as municipios
from dash.mapa_arco import gerar_pydeck

#para deploy no st cloud vou ler direto o arquivo csv
df_casamentos = casamamentos()
df_municipios = municipios()

import pandas as pd

mapa_arco = gerar_pydeck(df_casamentos)

st.title('Casamentos da cidade de São Paulo')
st.pydeck_chart(mapa_arco)


COD_MUNICIPIO = df_municipios.sample(1)['cod_municipio'].values[0]

df_selecionado = df_municipios[df_municipios['cod_municipio']==COD_MUNICIPIO].reset_index(drop=True)

st.text(f'Selecionado: {COD_MUNICIPIO}')
st.dataframe(df_selecionado)