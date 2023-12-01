from core.ckan_api_reader import Ckan
from config import CKAN_DOMAIN
from typing import Generator

class Extract:

    def __init__(self):

        self.ckan = Ckan(CKAN_DOMAIN)
    
    def get_resource_mdata(self)->list:

        resources = self.ckan('pib-municipal-2002-2020', 
                 search_string='pib (para os|por) munic(i|í)pio',
                 how='regex',
                 as_list=True, format_=['xlsx', 'xls'])

        return resources

    def xls_gen(self)->Generator:

        resources = self.ckan('pib-municipal-2002-2020', 
                 search_string='pib (para os|por) munic(i|í)pio',
                 how='regex',
                 as_list=False,
                 extract=True,
                 format_=['xlsx', 'xls'])

        return resources
    
    def extract_anos(self, resource_list:list=None)->list:
        
        if resource_list is None:
            resource_list = self.get_resource_mdata()

        anos = [r['name'].lower().split('pib')[-1].strip() 
                for r in resource_list]
        
        return anos



