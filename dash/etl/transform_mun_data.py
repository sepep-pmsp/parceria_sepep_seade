from .extract_mun_data import Extractor
import pandas as pd
from typing import Tuple

class Transformer:

    package = 'populacao-municipal-2010-2022'
    resource = '2021'
    filter_column = 'ano'
    filter_rows = 2021
    column_mapper = {
    'cod_ibge' : 'cod_municipio',
    'populacao' : 'habitantes',
}

    def __init__(self) -> None:

        

        self.extractor = Extractor()



    def rename_and_filter_columns(self):



        df = self.extractor.get_specified_package_with_resources(self.package, self.resource)
        df = df[(df[self.filter_column] == self.filter_rows)]

        df = df[self.column_mapper.keys()].rename(self.column_mapper, axis=1)
        
        df= df.reset_index(drop=True)

        return df
