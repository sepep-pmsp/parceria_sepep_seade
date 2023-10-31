from .base_transform import Base
from pandas import DataFrame

class Transform(Base):

    def pipeline(self)->DataFrame:

        df = self.extract.codigos_mun
        df = self.custom_filter_rows(df)
        df = self.filter_columns(df, ['cod_pais', 'nome_pais', 'ra_desc', 'rm_desc'])
        df = self.rename_columns(df, 'cod_pais', nome_pais='nome_municipio', ra_desc='regiao_administrativa', rm_desc= 'regiao_metropolitana' )

        return df
    
    def custom_filter_rows(self, df: DataFrame) -> DataFrame:
        filtered_df = df[(df['ra_desc'] != 'SP - Município ignorado') & (df['uf'] == 35)]
        return filtered_df
    
    
    def __call__(self)->DataFrame:

        return self.pipeline()
    