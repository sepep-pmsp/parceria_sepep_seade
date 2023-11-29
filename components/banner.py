from dash import dcc, html, dash_table



class Banner:
    def __init__(self):

        self.titulo_div = html.H1('Casamentos em São Paulo',
                        className='texto_logo')
        self.logo_div = html.Img(src= './assets\LOGOTIPO_PREFEITURA_HORIZONTAL_MONOCROMÁTICO_NEGATIVO.png',
                        className='imagem_logo')
        

    def criar_componente_final(self):
        self.banner_div = html.Div([self.titulo_div, self.logo_div],
                        className='banner_div')
        
    def pipeline(self):
        
        banner = self.criar_componente_final()

        return banner
    
    def __call__(self)-> html.Div:

        return self.pipeline()
