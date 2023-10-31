from .transform import Transformer
import pandas as pd
from utils.path import check_file_exists, solve_path
from config import DATA_FOLDER

class Load:

    file_name = 'casamentos_final.parquet'

    def __init__(self, verbose=True):

        self.transform = Transformer(verbose)

        self.df_gen = self.transform()
        self.file_name_path = solve_path(DATA_FOLDER, self.file_name)

    def pipeline(self):

        final = []
        for df in self.df_gen:
            final.append(df)
        
        df_final = pd.concat(final)
        del final

        df_final.to_parquet(self.file_name_path)

        return df_final
    
    def load(self)->pd.DataFrame:

        if check_file_exists(self.file_name_path):
            return pd.read_parquet(self.file_name_path)
        
        return self.pipeline()
    
    def __call__(self):

        return self.load()