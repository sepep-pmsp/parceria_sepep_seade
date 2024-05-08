import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import json
from dash import html
from etls.scripts.municipios import etl as municipios
from components.layout import Layout

import os

domain = os.getenv('PUBLIC_DOMAIN')
api_path = os.getenv('API_PATH')
protocol = os.getenv('DEFAULT_PROTOCOL')
url = f'{protocol}://{domain}{api_path}/docs'

external_stylesheets = [
    dbc.themes.CYBORG, 'https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap', dbc.icons.FONT_AWESOME]
layout = Layout()


def servir_layout():
    return layout()


def reciclar_layout(div):
    return html.Div([html.Div([layout.mapa_div, layout.dropdown_com_grafico_div], className='map_and_graph', ),
                          layout.outros_graficos_div, html.Div([div], className='Modal')], className='hero')


link_api = html.Span(html.A('aqui', href=url), className='span_data')
link_repo_seade = html.Span(
    html.A('aqui', href='https://repositorio.seade.gov.br/', className='span_data'))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
df_municipios = municipios()
app.layout = servir_layout


@app.callback(Output('seletor_mun', "value"), [Input("deck-gl", 'clickInfo'), Input('seletor_mun', 'value')])
def get_mun_name(data, selecao_atual):

    if data:
        # puxa o municipio, caso tenha clicado fora já define como miss
        objeto = data.get('object') or {'destino': selecao_atual}

        selecao = objeto.get('destino', selecao_atual)
        return selecao
    return selecao_atual


@app.callback(Output('deck-gl', 'clickInfo'), Input('seletor_mun', 'value'))
def zerar_dados_mapa(valor):

    return None


@app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([html.Div([layout.mapa_div, layout.dropdown_com_grafico_div], className='map_and_graph', ),
                          layout.outros_graficos_div,], className='hero')

    elif pathname == "/about":
        texto_sobre_1 = '''Este dashboard é fruto de uma parceria entre a Secretaria Executiva de Planejamento e Entregas Prioritárias, da Prefeitura de São Paulo, e a Fundação SEADE, do Governo do Estado de São Paulo.
        Além desse dashboard, essa parceria permitiu a reorganização dos dados no repositório público disponibilizado pela SEADE, o consumo periódico automatizado de alguns desses dados e a modelagem para a disponibilização destes via API REST.
        O repositório da SEADE pode ser acessado '''
        texto_sobre_2 = ' e a API REST pode ser acessada '

        return reciclar_layout(html.Div(
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H1('Sobre'),
                            html.P(
                                [
                                    texto_sobre_1,
                                    link_repo_seade,
                                    texto_sobre_2,
                                    link_api,
                                    '.'
                                ])
                         ],
                    ),
                    style={"width": "104rem"}, id='card_collapse'),
                id="horizontal-collapse",
                is_open=False,
                dimension="width",
            ),
            style={'minHeight': '100%'},
            className='body_card_div'))

    elif pathname == "/data":
        texto_dados = '''Os dados apresentados neste dashboard foram inicialmente coletados por por meio da API do CKAN mantido pela Fundação SEADE, abrangendo diversas fontes, como Microdados de casamentos ocorridos nos municípios do Estado de São Paulo, População por municípios de 2000 a 2021, PIB Municipal de 2002 a 2020, estatísticas de Nascidos Vivos por sexo em 2021, Nascidos Vivos de 2000 a 2020 e a Tabela de município/UF/País.
Após a extração destes dados via API, realizamos diversas etapas de processamento para garantir a qualidade e uniformidade das informações. Inicialmente, renomeamos as colunas visando padronizar a estrutura dos dados finais. Posteriormente, procedemos à filtragem mantando apenas casamentos realizados entre pessoas do município de São Paulo e indivíduos de outros municípios do estado de São Paulo. Após essas transformações, os dados tratados para gerar as visualizações disponíveis neste dashboard. Esses dados também estão acessíveis por meio de nossa API, disponível '''
        return reciclar_layout(html.Div(
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody([html.H1('Dados'), html.P([texto_dados, link_api, '.'])], class_name= 'texto_data',
                    ),
                    style={"width": "104rem"}, id='card_collapse'
                ),
                id="horizontal-collapse_data",
                is_open=False,
                dimension="width",
            )))


    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="hero p-3 bg-light rounded-3",
    )

@ app.callback(
    Output("horizontal-collapse_data", "is_open"),
    [Input("horizontal-collapse-button_data", "n_clicks")],
    [State("horizontal-collapse_data", "is_open")],
)
def toggle_collapse(n, is_open):

    return True

@ app.callback(
    Output("horizontal-collapse", "is_open"),
    [Input("horizontal-collapse-button", "n_clicks")],
    [State("horizontal-collapse", "is_open")],
)
def toggle_collapse(n, is_open):

    return True


@ app.callback(
    Output("grafico_linha_hab", "figure"),
    Input("seletor_mun", "value"))
def update_line_chart_habitantes(cod_mun):

    mask=df_municipios['cod_municipio'] == cod_mun
    fig=px.line(df_municipios[mask],
        x="Ano", y="Habitantes do Município", title='Habitantes do munícipio')
    fig.update_layout(template='plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono")
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)


    return fig


@ app.callback(
    Output("grafico_linha_nascidos_vivos", "figure"),
    Input("seletor_mun", "value"))
def update_line_chart_nascidos_vivos(cod_mun):

    mask=df_municipios['cod_municipio'] == cod_mun
    fig=px.line(df_municipios[mask],
        x="Ano", y="Nascidos vivos", title='Número de nascituros')
    fig.update_layout(template='plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono")
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)



    return fig


@ app.callback(
    Output("grafico_linha_pib", "figure"),
    Input("seletor_mun", "value"))
def update_line_chart_pib(cod_mun):

    mask=df_municipios['cod_municipio'] == cod_mun
    fig=px.line(df_municipios[mask],
        x="Ano", y="Valor do PIB", title='Valor do PIB')
    fig.update_layout(template='plotly_dark',)
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)', font_family="Roboto Mono")
    fig.update_traces(line_color='rgba(240, 100, 0, 40)', line_width=5)

    return fig

server=app.server

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
