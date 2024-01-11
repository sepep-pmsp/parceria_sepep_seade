import pandas as pd
from functools import partial
from config import DATA_FOLDER
from api_core.core.utils.fpath import files_by_extension, solve_path

class LoadPibCSV:

    data_folder = 'pib_municipal'

    def __init__(self):

        self.data_folder = self.solve_data_folder()
        self.file = self.get_csv()

    def solve_data_folder(self)->None:

        return solve_path(self.data_folder, DATA_FOLDER)

    def get_csv(self, path:str=None)->str:

        if path is None:
            path = self.data_folder

        csvs = files_by_extension(path, '.csv')
        todos_anos = [f for f in csvs if 'pib_municipal_todos_anos' in f]

        return todos_anos[0]


    def load_csv(self)->pd.DataFrame:

        df = pd.read_csv(self.file, sep=';', encoding='latin-1')
        
        return df

    def cols_to_lower(self, cols):

        rename = {col : col.lower() for col in cols}

        return rename


    def lower_cols(self, df:pd.DataFrame)->pd.DataFrame:

        rename_map = self.cols_to_lower(df.columns)
        df.rename(rename_map, axis=1, inplace=True)

    def __call__(self):

        df = self.load_csv()
        self.lower_cols(df)

        return df