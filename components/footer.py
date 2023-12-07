from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

class Footer:
    def __init__(self):

        self.footer = dbc.Card([html.Footer([html.H3('Códigos desenvolvidos no âmbito da parceria entre CAGI/SEPEP/PMSP e SEADE/Estado de São Paulo (processo SEI 6011.2022/0002067-1).'), 
                                             
                                            html.Div([html.Img(src='	https://www.seade.gov.br/wp-content/themes/byvex-child/assets/images/logo-seade-home.svg', className='img'),html.Img(src='https://smae.prefeitura.sp.gov.br/assets/img/Logo%20SEPEP%20-%20Branco.svg', className='img'),html.Img(src='	https://smae.prefeitura.sp.gov.br/assets/img/GOVERNO_HORIZONTAL_FUNDO_ESCURO.png',className='img'), ],className='imagens_footer')
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

