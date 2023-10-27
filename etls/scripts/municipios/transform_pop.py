from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def pipeline(self)->DataFrame:

        df = self.extract.populacao
        df = self.filter_rows(df, 'ano', 2021)
        df = self.filter_columns(df, ['cod_ibge', 'populacao'])
        df = self.rename_columns(df, 'cod_ibge', populacao='habitantes')

        return df
    
    def __call__(self)->DataFrame:

        return self.pipeline()
