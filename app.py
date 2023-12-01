import dash
from dash.dependencies import Input, Output
import plotly.express as px

from etls.scripts.municipios import etl as municipios

from components.layout import Layout

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap']

app = dash.Dash(__name__, external_stylesheets= external_stylesheets)
df_municipios = municipios()

layout = Layout()


    

def servir_layout():
    return layout.pipeline()

app.layout = servir_layout


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
        x="Ano", y="Habitantes do Município", title='Habitantes do munícipio')
    fig.update_layout( template= 'plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono")
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
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono")
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)



    return fig


@app.callback(
    Output("grafico_linha_pib", "figure"), 
    Input("seletor_mun", "value"))
def update_line_chart_pib(cod_mun):

    mask = df_municipios['cod_municipio']==cod_mun
    fig = px.line(df_municipios[mask], 
        x="Ano", y="Valor do PIB", title= 'Valor do PIB')
    fig.update_layout( template= 'plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono")
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)