from etls.utils import save_df_as_csv, solve_path
from config import DATA_FOLDER
from functools import partial
import pandas as pd


class Load:

    def __init__(self)->None:

        self.data_folder = solve_path('pib_municipal', parent=DATA_FOLDER)
        self.save_df_as_csv = partial(save_df_as_csv, folder=self.data_folder, 
                            encoding='cp-1252', decimal=',')

    
    def solve_csv_fname(self, ano: str, fname:str)->str:

        if fname is None and ano is None:
            raise ValueError('Either ano or fname must be passed')

        if fname is None:
            fname = f'pib_municipal_{ano}.csv'
            return fname
        
        if not fname.endswith('.csv'):
            fname = fname + '.csv'
        return fname


    def dump_to_csv(self, df: pd.DataFrame, ano: str=None, fname: str = None)->None:

        fname = self.solve_csv_fname(ano, fname)

        self.save_df_as_csv(df, 
                            fname, 
                            sep=';',
                            encoding='latin-1',
                            index=False)

