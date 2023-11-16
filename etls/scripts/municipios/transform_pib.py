from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def replace_money_format(self, df:DataFrame)->DataFrame:

        col_pib = 'valor_do_PIB'
        df = df.copy()
        df[col_pib] = df[col_pib].str.replace('R$', '', regex=False)
        #left strip para remover espaço a esquerda
        df[col_pib] = df[col_pib].str.lstrip()

        return df
    
    def string_to_int(self, df:DataFrame, col:str)->DataFrame:

        df = df.copy()
        #string está como numero br, tem que dar replace nos pontos
        df[col] = df[col].str.replace('.', '')
        df[col] = df[col].str.replace(',', '.')

        df[col] = df[col].astype(float)

        return df
    
    def format_valor_pib(self, df:DataFrame)->DataFrame:

        df = self.replace_money_format(df)
        df = self.string_to_int(df, 'valor_do_PIB')

        return df

    def pipeline(self)->DataFrame:

        df = self.extract.pib
        df = self.filter_rows(df, 'Setor', 'PIB')
        df = self.filter_columns(df, ['Cod_Ibge', 'Valor', 'Ano'])
        df = self.rename_columns(df, 'Cod_Ibge', Valor='valor_do_PIB')
        df = self.format_valor_pib(df)

        df = df.sort_values(['cod_municipio','Ano'])


        return df
    
    
    def __call__(self)->DataFrame:

        return self.pipeline()
    