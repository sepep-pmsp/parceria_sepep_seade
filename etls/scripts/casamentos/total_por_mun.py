import pandas as pd

class TransformTotalMun:

    def __init__(self, df_casamentos:pd.DataFrame)->None:


        self.df_original = self.remover_null_mun(df_casamentos)


    def remover_null_mun(self, df:pd.DataFrame)->pd.DataFrame:

        return df[df['nome_municipio_destino'].notnull()].reset_index(drop=True)
    
    def agrupar_por_mun(self)->pd.DataFrame:

        casamentos_total = self.df_original.groupby('nome_municipio_destino')[['total_casamentos']].sum()
        
        return casamentos_total.reset_index()
    
    @property
    def vars_qualificadoras_mun(self):

        return [col for col in self.df_original.columns if col not in ('total_casamentos', 'ano')]
    

    def dropar_duplicados(self, df_dados:pd.DataFrame)->pd.DataFrame:

        #dropar dados duplicados
        df_dados = df_dados.drop_duplicates()

        return df_dados
    
    @property
    def dados_municipios(self):

        dados_mun = self.df_original[self.vars_qualificadoras_mun]
        return self.dropar_duplicados(dados_mun)
    
    def adicionar_cols_mun(self, df_agrupado:pd.DataFrame)->pd.DataFrame:

        com_dados = pd.merge(df_agrupado, self.dados_municipios, on='nome_municipio_destino', how='left')
        

        return com_dados

    def pipeline(self):

        agrupado = self.agrupar_por_mun()
        com_dados = self.adicionar_cols_mun(agrupado)

        return com_dados

    def __call__(self):

        return self.pipeline()