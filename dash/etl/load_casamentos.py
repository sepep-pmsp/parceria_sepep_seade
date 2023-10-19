from .transform_casamentos import Transformer
import os
import pandas as pd
from config import DATA_FOLDER

class Load:

    file_name = 'casamentos_final.parquet'

    def __init__(self, verbose=True):

        self.transform = Transformer(verbose)

        self.df_gen = self.transform()
        self.file_name_path = os.path.join(DATA_FOLDER, self.file_name)

    def check_file_exists(self):

        return os.path.exists(self.file_name_path)
    
    def pipeline(self):

        final = []
        for df in self.df_gen:
            final.append(df)
        
        df_final = pd.concat(final)
        del final

        df_final.to_parquet(self.file_name_path)

        return df_final
    
    def load(self)->pd.DataFrame:

        if self.check_file_exists():
            return pd.read_parquet(self.file_name_path)
        
        return self.pipeline()
    
    def __call__(self):

        return self.load()