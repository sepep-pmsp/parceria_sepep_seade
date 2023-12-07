from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

class Footer:
    def __init__(self):

        self.footer = dbc.Card([html.Footer([html.H3('Códigos desenvolvidos no âmbito da parceria entre CAGI/SEPEP/PMSP e SEADE/Estado de São Paulo (processo SEI 6011.2022/0002067-1).'), 
                                             html.P('ACORDO DE COOPERAÇÃO TÉCNICA sem transferência de recursos entre PREFEITURA DO MUNICÍPIO DE SÃO PAULO, por intermédio da SECRETARIA DE GOVERNO MUNICIPAL – SGM e sua SECRETARIA EXECUTIVA DE PLANEJAMENTO E ENTREGAS PRIORITÁRIAS – SGM/SEPEP e A FUNDAÇÃO SISTEMA ESTADUAL DE ANÁLISE DE DADOS - SEADE. para cooperação e conjugação de esforços visando ao desenvolvimento de atividades de mútuo interesse na área de Ciência de Dados.')
                                            ,
                                             ])])


    def criar_componente_final(self):
        footer_div = html.Div(self.footer,
                                     )
        return footer_div
        
    def pipeline(self):
        
        footer = self.criar_componente_final()

        return footer
    
    def __call__(self)-> html.Div:

        return self.pipeline()

