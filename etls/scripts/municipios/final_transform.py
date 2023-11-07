from .transform_mun import Transform as Transform_mun
from .transform_nasc import Transform as Transform_nasc
from .transform_pib import Transform as Transform_pib
from .transform_pop import Transform as Transform_pop
import pandas as pd
import copy
import itertools as itertools


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

        dataframes_instances = [df for df in self.dataframes.values()]
        #O primeiro dataframe sempre será o de municipios,
        # que precisa ser o primeiro ao iniciar a funcao
        pivot = dataframes_instances.pop(0)
        print(dataframes_instances)

        set_ano = set()
        for df in dataframes_instances:
            temp_set = set(df['Ano'].unique())
            set_ano = set_ano.union(temp_set)



        set_mun = set(pivot['cod_municipio'])


        new_df_data = [(ano, cod_mun) for ano, cod_mun in itertools.product(set_ano, set_mun)]
        new_df_columns = ['Ano', 'cod_municipio']

        new_df = pd.DataFrame(data= new_df_data, columns= new_df_columns)

        pivot = pd.merge(pivot, new_df, how='left', on=['cod_municipio'])



        for df in dataframes_instances: 
            #o merge vai ter que ser no cod_municipio + ano
            df['cod_municipio'] = df['cod_municipio'].astype(int)
            pivot = pd.merge(pivot, df, how='left', on=['cod_municipio', 'Ano'])

                    

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

