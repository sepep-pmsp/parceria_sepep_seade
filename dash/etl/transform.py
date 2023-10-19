from .extract import Extractor
import pandas as pd

class Transformer:

    colunas_mapper = {
        'anoreferencia' : 'ano_casamento',
        'codrescj1' : 'cod_residencia_cj1',
        'codrescj2' : 'cod_residencia_cj2',
        'codmunreg' : 'municipio_realiz_casamento'
    }

    codigo_ibge_estado_sp = 35
    codigo_ibge_cidade_sp = 3550308

    def __init__(self):

        self.extract = Extractor()
        self.resources_gen = self.extract()

    def filter_cols(self, df:pd.DataFrame)->pd.DataFrame:

        return df[self.colunas_mapper.keys()]
    
    def rename_cols(self, df:pd.DataFrame)->pd.DataFrame:

        return df.rename(self.colunas_mapper, axis=1)
    

    def filtrar_casamentos_paulistanos(self, df:pd.DataFrame)->pd.DataFrame:

        filtro = ((df['cod_residencia_cj1']==self.codigo_ibge_cidade_sp)|
                  (df['cod_residencia_cj2']==self.codigo_ibge_cidade_sp))
        
        df_filtrado = df[filtro].copy().reset_index(drop=True)

        return df_filtrado