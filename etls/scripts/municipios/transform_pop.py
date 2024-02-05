from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def pipeline(self)->DataFrame:

        df = self.extract.populacao
        df = self.filter_columns(df, ['cod_ibge', 'pop_total', 'ano'])
        df = self.rename_columns(df, 'cod_ibge', pop_total='Habitantes do Município', ano='Ano')

        df = df.sort_values(['cod_municipio','Ano'])
        df = df.dropna()


        return df
    
    def __call__(self)->DataFrame:

        return self.pipeline()
