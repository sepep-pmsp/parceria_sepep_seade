from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def pipeline(self) -> DataFrame:
        df = self.extract.codigos_mun
        df = self.custom_filter_rows(df, 'Ano', 2021)
        df = self.filter_columns(df, ['Código IBGE', 'Nascidos vivos'])
        df = self.rename_columns(df, 'Código IBGE', estats_vitais='habitantes')
        return df

    def custom_filter_rows(self, df: DataFrame, column: str, value: any) -> DataFrame:
        filtered_df = df[(df['ra_desc'] != 'SP - Município ignorado') & (df['uf'] == 35)]
        return filtered_df

    def __call__(self) -> DataFrame:
        return self.pipeline()