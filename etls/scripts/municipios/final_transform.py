from .transform_mun import Transform as Transform_mun
from .transform_nasc import Transform as Transform_nasc
from .transform_pib import Transform as Transform_pib
from .transform_pop import Transform as Transform_pop
import pandas as pd
import copy

class Transformer:


    dataframes = {
        'mun' : 'transform_mun',
        'pib' : 'transform_pib',
        'pop' : 'transform_pop',
        'nasc' : 'transform_nasc'
    }

    def __init__(self):

        self.dataframes = copy.deepcopy(self.dataframes)
        self.transform_mun = Transform_mun()
        self.transform_pib = Transform_pib()
        self.transform_pop = Transform_pop()
        self.transform_nasc = Transform_nasc()



    def get_transformed_dataframes(self)->pd.DataFrame:

        for df_name, method in self.dataframes.items():
            transform = getattr(self, method)
            self.dataframes[df_name] = transform()

    def merge_dataframes(self)->pd.DataFrame:

        dataframes = [df for df in self.dataframes.values()]
        pivot = dataframes.pop()

        for df in dataframes: 
            df['cod_municipio'] = df['cod_municipio'].astype(int)
            pivot = pd.merge(pivot, df, how='left', on='cod_municipio')

        return pivot
    
    def remove_estado_sp(self, merged_df:pd.DataFrame)->pd.DataFrame:

        filtro_sp = merged_df['cod_municipio']==3500000
        df = merged_df[~filtro_sp].reset_index(drop=True)

        return df
    
    def pipeline(self)->pd.DataFrame:

        self.get_transformed_dataframes()
        df = self.merge_dataframes()
        df = self.remove_estado_sp(df)

        return df
    
    def __call__(self)->pd.DataFrame:

        return self.pipeline()





        





# result_dfs = []

# dfs = [a,b,c,d]

# for df in dfs: 
#     result = df.pipeline()
#     result_dfs.append(result)

# pivot = a.pipeline().copy()

# for df in result_dfs:
#     df['cod_municipio'] = pivot['cod_municipio'].astype(int)
#     pivot = pd.merge(pivot, df, how='left', on='cod_municipio')

