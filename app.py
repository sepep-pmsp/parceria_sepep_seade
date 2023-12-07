import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import json
from dash import html
from etls.scripts.municipios import etl as municipios
from components.layout import Layout

external_stylesheets = [ dbc.themes.CYBORG, 'https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap', dbc.icons.FONT_AWESOME]
layout = Layout()

def servir_layout():
    return layout()

def reciclar_layout(div):
    return html.Div([html.Div([layout.mapa_div, layout.dropdown_com_grafico_div], className='map_and_graph', ),
                          layout.outros_graficos_div, html.Div([div], className='Modal')],className='hero')

app = dash.Dash(__name__, external_stylesheets= external_stylesheets, suppress_callback_exceptions=True)
df_municipios = municipios()
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
        Output("page-content", "children"), 
        [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return html.Div([html.Div([layout.mapa_div, layout.dropdown_com_grafico_div], className='map_and_graph', ),
                          layout.outros_graficos_div,],className='hero')
                          

    elif pathname == "/about":
        return reciclar_layout(html.Div(
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody([html.H1('Sobre'),html.P("Voluptate amet nulla commodo non ea in ullamco anim labore cupidatat. Voluptate amet nulla commodo non ea in ullamco anim labore cupidatat. Voluptate amet nulla commodo non ea in ullamco anim labore cupidatat. Voluptate amet nulla commodo non ea in ullamco anim labore cupidatat. Voluptate amet nulla commodo non ea in ullamco anim labore cupidatat. Voluptate amet nulla commodo non ea in ullamco anim labore cupidatat. Voluptate amet nulla commodo non ea in ullamco anim labore cupidatat.")],
                        
                    ),
                    style={"width": "104rem"}, id='card_collapse'
                ),
                id="horizontal-collapse",
                is_open=False,
                dimension="width",
            ),
            style={'minHeight' : '100%'},
        className= 'body_card_div'))
    

    elif pathname == "/data":
        return reciclar_layout(html.Div(
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody([html.H1('Dados'),html.P("Culpa dolore adipisicing commodo voluptate tempor non laboris sit consectetur officia voluptate laboris laborum.")],
                        
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

@app.callback(
    Output("horizontal-collapse_data", "is_open"),
    [Input("horizontal-collapse-button_data", "n_clicks")],
    [State("horizontal-collapse_data", "is_open")],
)
def toggle_collapse(n, is_open):
    
    return True

@app.callback(
    Output("horizontal-collapse", "is_open"),
    [Input("horizontal-collapse-button", "n_clicks")],
    [State("horizontal-collapse", "is_open")],
)
def toggle_collapse(n, is_open):

    return True


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