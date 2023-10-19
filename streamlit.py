import streamlit as st
#from dash.etl.load_casamentos import Load
from dash.mapa_arco import gerar_pydeck

#para deploy no st cloud vou ler direto o arquivo csv
#load = Load()

import pandas as pd

df = pd.read_csv('dados_final.csv')
mapa_arco = gerar_pydeck(df)

st.title('Casamentos da cidade de São Paulo')
st.pydeck_chart(mapa_arco)
