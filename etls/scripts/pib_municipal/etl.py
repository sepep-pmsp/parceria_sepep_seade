from .extract import Extract
from .transform import Transform
from .load import Load
from ..base_etl_class import ETL

import pandas as pd

class ETL(ETL):

    def __init__(self):

        self.extract = Extract()
        self.transform = Transform()
        self.load = Load()

    def save_as_csvs(self)->None:

        anos = self.extract.extract_anos()
        df_gen = self.extract.xls_gen()
        for ano in anos:
            df = next(df_gen)
            df = self.transform(df, ano)
            self.load.dump_to_csv(df, ano)

    def concat_dataframes(self)->pd.DataFrame:

        parsed_dfs = []

        anos = self.extract.extract_anos()
        df_gen = self.extract.xls_gen()
        for ano in anos:
            df = next(df_gen)
            df = self.transform(df, ano)
            parsed_dfs.append(df)

        return pd.concat(parsed_dfs)

    def save_as_single_csv(self, df:pd.DataFrame=None)->None:

        if df is None:
            df = self.concat_dataframes()
        self.load.dump_to_csv(df, 'pib_municipal_todos_anos')

    def map_parameters(self, save_csvs, save_single_csv, return_df):

        if save_csvs:
            self.save_as_csvs()
            return
        
        if save_single_csv:
            self.save_as_single_csv()
            return

        if return_df and save_single_csv:
            df = self.concat_dataframes()
            self.save_as_single_csv(df)
            return df

        if return_df:
            return self.concat_dataframes()

        raise ValueError('Must define the load method.')



    def __call__(self, save_csv = False, save_single_csv=False, return_df=False):

        
        return self.map_parameters(save_csv, save_single_csv, return_df)

                
