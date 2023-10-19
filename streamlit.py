import streamlit as st
from dash.etl.load_casamentos import Load
from dash.mapa_arco import gerar_pydeck

load = Load()

df = load()
mapa_arco = gerar_pydeck(df)

st.title('Casamentos da cidade de São Paulo')
st.pydeck_chart(mapa_arco)
