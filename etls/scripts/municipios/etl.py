from .load import Load
from ..base_etl_class import ETL

class ETL(ETL):

    def __init__(self):

        self.load = Load()

    def __call__(self):

        return self.load()