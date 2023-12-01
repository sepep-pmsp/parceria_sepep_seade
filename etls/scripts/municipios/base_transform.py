from .extract import Extractor
import pandas as pd
from typing import List

class Base:

   def __init__(self):

      self.extract = Extractor()

   def build_filter(self, df:pd.DataFrame, column:str, value:any)->pd.DataFrame:
      
      return (df[column]==value)
   
   def filter_rows(self, df:pd.DataFrame, column:str, value:any)->pd.DataFrame:
      
      filter = self.build_filter(df, column, value)
      
      return df[filter].copy().reset_index(drop=True)
   
   def filter_columns(self, df:pd.DataFrame, columns:List[str])->pd.DataFrame:
      
      return df[columns].copy()
   
   def rename_columns(self, df:pd.DataFrame, col_cod:str, **col_renames)->pd.DataFrame:
      
      col_renames[col_cod] = 'cod_municipio'

      df = df.rename(col_renames, axis=1)

      return df
   


