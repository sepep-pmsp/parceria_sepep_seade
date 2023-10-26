from core.ckan_api_reader import Ckan
import pandas as pd
from config import CKAN_DOMAIN
from typing import Generator


class Extractor:

    def __init__(self, domain: str = CKAN_DOMAIN) ->None:
        self.ckan = Ckan(domain)

    def check_available_packages(self) -> Generator:

        package_list = self.ckan.pkgs
        return package_list
    
    def get_specified_package_with_resources(self,package,resource) -> Generator:
        
        result = next(
                    self.ckan(package, 
                         as_list=False,
                         extract=True, 
                         search_string=resource, 
                         attr='name', 
                         how='contains', 
                         parser_params={'sep' : ';'})
        )
        return result

    def __call__(self) -> Generator:

        return self.get_specified_package_with_resources()
