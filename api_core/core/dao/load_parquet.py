import pandas as pd

from config import DATA_FOLDER
from api_core.core.utils.fpath import files_by_extension, solve_path


class LoadParquet:

    def format_filename(self, filename:str)->str:

        if not filename.endswith('.parquet'):
            raise ValueError('Must be parquet file!')
        
        return solve_path(filename, DATA_FOLDER)
    
    def find_parquet_files(self)->str:

        files = files_by_extension(DATA_FOLDER, '.parquet')

        return files
    
    def match_file(self, filename:str)->str:

        files = self.find_parquet_files()
        filename = self.format_filename(filename)
        for file in files:
            if file == filename:
                return file
        else:
            raise ValueError(f'File {filename} não encontrada no diretório de dados {DATA_FOLDER}')

    def read_parquet(self, filename:str)->pd.DataFrame:

        return pd.read_parquet(filename)
    
    def __call__(self, filename:str)->pd.DataFrame:
        
        file_name = self.match_file(filename)

        df = self.read_parquet(file_name)

        return df