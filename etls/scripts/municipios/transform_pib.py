from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def pipeline(self)->DataFrame:

        df = self.extract.pib
        df = self.filter_rows(df, 'Setor', 'PIB')
        df = self.filter_columns(df, ['Cod_Ibge', 'Valor'])
        df = self.rename_columns(df, 'Cod_Ibge', pib='Valor')

        return df
    
    def __call__(self)->DataFrame:

        return self.pipeline()
    