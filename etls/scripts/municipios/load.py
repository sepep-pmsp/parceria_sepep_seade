from .final_transform import Transformer
import pandas as pd
from etls.utils.path import check_file_exists, solve_path
from config import DATA_FOLDER

class Load:

    file_name = 'municipios_final.parquet'

    def __init__(self):

        self.transform = Transformer()
        self.file_name_path = solve_path(self.file_name, DATA_FOLDER)

    def pipeline(self):

        df_final = self.transform()
        df_final.to_parquet(self.file_name_path)

        return df_final
    
    def load(self, use_existing_file)->pd.DataFrame:

        if use_existing_file and check_file_exists(self.file_name_path):
            return pd.read_parquet(self.file_name_path)
        
        return self.pipeline()
    
    def __call__(self, use_existing_file):

        return self.load(use_existing_file)
