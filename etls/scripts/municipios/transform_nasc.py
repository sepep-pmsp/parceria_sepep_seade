from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def pipeline(self) -> DataFrame:
        df = self.extract.estats_vitais
        df = self.filter_rows(df, 'Ano', 2021)
        df = self.filter_columns(df, ['Código IBGE', 'Nascidos vivos'])
        df = self.rename_columns(df, 'Código IBGE', estats_vitais='Nascidos vivos')
        return df


    def __call__(self) -> DataFrame:
        return self.pipeline()