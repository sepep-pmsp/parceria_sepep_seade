from core.ckan_api_reader import Ckan
from config import CKAN_DOMAIN


class Extractor:

    pkg_name = 'microdados-casamentos'

    def __init__(self, domain=CKAN_DOMAIN):

        self.ckan = Ckan(domain)

    
    def list_resources(self):

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
