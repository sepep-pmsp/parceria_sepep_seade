import pandas as pd
from functools import partial
from .load_pib_csv import LoadPibCSV

class PibCSVDAO:

    def __init__(self):

        self.load_csv = LoadPibCSV()
        self.df = self.load_csv()
        self.__set_methods()

    def __mask_ano(self, df:pd.DataFrame, ano: int)->pd.Series:

        mask_ano = df['ano'].astype(int)==ano

        return mask_ano

    def __mask_municipio(self, df:pd.DataFrame, mun_name:str)->pd.Series:

        mask_municipio = df['municipio']==mun_name

        return mask_municipio

    def __df_to_dict(self, df:pd.DataFrame)->pd.DataFrame:

        return df.to_dict(orient='records')

    def __filter_municip_ano(self, df:pd.DataFrame, municipio:str, ano:int):

        if ano:
            mask_ano = self.__mask_ano(df, ano)
            df = df[mask_ano]
        if municipio:
            mask_municip = self.__mask_municipio(df, municipio)
            df = df[mask_municip]

        return df

    def __check_col_name(self, col_name:str)->None:

        cols = self.df.columns
        if col_name not in cols:
            raise ValueError(f'col_name must be in {cols}')

    def __standardize_value_col(self, df:pd.DataFrame, col_name:str)->pd.DataFrame:

        df.rename({col_name:'valor'},axis=1, inplace=True)

    def __get_dimension(self, df:pd.DataFrame, col_name:str, standardize:bool=True)->pd.DataFrame:

        self.__check_col_name(col_name)
        cols = ['municipio', 'ano']
        cols.append(col_name)
        df = df[cols]
        if standardize:
            self.__standardize_value_col(df, col_name)

        return df

    def __only_kwrd_args(self, _):

        if len(_)>0:
            raise ValueError('Only keyword args allowed')

    def __base_call(self, *_, municipio:str=None, ano:int=None, dimension: str=None):


        self.__only_kwrd_args(_)
        df = self.df.copy()
        df = self.__filter_municip_ano(df, municipio, ano)
        
        if dimension:
            df = self.__get_dimension(df, dimension)
        json = self.__df_to_dict(df)

        return json

    def __set_partial_call(self, dimension:str)->None:
        
        self.__check_col_name(dimension)
        partial_m = partial(self.__base_call, dimension=dimension)
        setattr(self, dimension.lower(), partial_m)

    def __set_all_call(self)->None:

        setattr(self, 'pib_all', self.__base_call)

    def __set_methods(self):

        self.__set_all_call()
        skip = {'municipio', 'ano'}
        for col in self.df.columns:
            if col not in skip:
                self.__set_partial_call(col)