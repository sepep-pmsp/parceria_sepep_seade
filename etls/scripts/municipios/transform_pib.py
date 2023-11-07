from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def pipeline(self)->DataFrame:

        df = self.extract.pib
        df = self.filter_rows(df, 'Setor', 'PIB')
        df = self.filter_columns(df, ['Cod_Ibge', 'Valor', 'Ano'])
        df = self.rename_columns(df, 'Cod_Ibge', Valor='valor_do_PIB')

        df = df.sort_values(['cod_municipio','Ano'])


        return df
    
    
    def __call__(self)->DataFrame:

        return self.pipeline()
    