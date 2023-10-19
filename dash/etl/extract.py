from core.ckan_api_reader import Ckan
from config import CKAN_DOMAIN
from typing import Generator

class Extractor:
    '''Extrai os recursos de microdados de casamentos.
    Retorna um generator de Dataframes'''

    pkg_name = 'microdados-casamentos'

    def __init__(self, domain:str=CKAN_DOMAIN)->None:

        self.ckan = Ckan(domain)

    
    def list_resources(self)->Generator:
        

        regex_resource = 'Microdados de casamentos ocorridos nos municípios do Estado de São Paulo - \d{4}'
        
        resources = self.ckan(self.pkg_name, 
                         as_list=False,
                         extract=True, 
                         search_string=regex_resource, 
                         attr='description', 
                         how='regex', 
                         case_sensitive=True,
                         parser_params={'sep' : ';'})
        
        return resources


    def __call__(self)->Generator:

        return self.list_resources()