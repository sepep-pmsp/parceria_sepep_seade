from .base_transform import Base
from pandas import DataFrame

import pandas as pd

class Transform(Base):

    def pipeline(self) -> DataFrame:
        df_2000 = self.extract.estats_vitais_2000_a_2020
        df_2021 = self.extract.estats_vitais_2021

        df_2021 = self.filter_columns(df_2021, ['Código IBGE', 'Nascidos vivos', 'Ano' ])

        df_2000 = self.rename_columns(df_2000, 'Cód. IBGE', estatisticas_vitais='Nascidos vivos')
        df_2021 = self.rename_columns(df_2021, 'Código IBGE', estatisticas_vitais='Nascidos vivos')

        
        df = pd.concat([df_2000, df_2021])

        df =  self.filter_columns(df, ['cod_municipio', 'Nascidos vivos', 'Ano' ]).reset_index(drop=True)
        df = df.sort_values(['cod_municipio','Ano'])
        return df


    def __call__(self) -> DataFrame:
        return self.pipeline()