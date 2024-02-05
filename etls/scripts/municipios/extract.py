from core.ckan_api_reader import Ckan
from config import CKAN_DOMAIN
from pandas import DataFrame

class Extractor:
    
    pacotes_busca = {
        'populacao' : {
            'nom_pkg' : 'populacao-residente-estado-de-sao-paulo',
            'search_str' : 'População 2000 - 2023',
                       },
        'pib' : {
            'nom_pkg' : 'pib-municipal-2002-2020',
            'search_str' : 'PIB Municipal 2002 a 2020'
            },
        'estats_vitais_2021' : {
            'nom_pkg' : 'estatisticas-vitais',
            'search_str' : 'Nascidos Vivos por sexo - 2021',
        },
        'estats_vitais_2000_a_2020' : {
            'nom_pkg' : 'estatisticas-vitais',
            'search_str' : 'Nascidos Vivos 2000-2020',
        },
        'codigos_mun' : {
            'nom_pkg' : 'microdados-casamentos',
            'search_str' : 'Tabela de município/UF/País'
        }
        
        
    }

    def __init__(self, domain: str = CKAN_DOMAIN) ->None:
        self.ckan = Ckan(domain)

    def get_specified_package_with_resources(self, nom_pkg:str, search_str:str) -> DataFrame:
        
        result = next(
                    self.ckan(nom_pkg, 
                         as_list=False,
                         extract=True, 
                         search_string=search_str, 
                         attr='name', 
                         how='contains', 
                         parser_params={'sep' : ';', 'thousands' : '.', 'decimal' : ','})
        )
        return result
    
    @property
    def populacao(self):

        return self.get_specified_package_with_resources(**self.pacotes_busca['populacao'])
    
    @property
    def pib(self):

        return self.get_specified_package_with_resources(**self.pacotes_busca['pib'])

    @property
    def estats_vitais_2021(self):

        return self.get_specified_package_with_resources(**self.pacotes_busca['estats_vitais_2021'])
    
    @property
    def estats_vitais_2000_a_2020(self):

        return self.get_specified_package_with_resources(**self.pacotes_busca['estats_vitais_2000_a_2020'])
    
    @property
    def codigos_mun(self):

        return self.get_specified_package_with_resources(**self.pacotes_busca['codigos_mun'])

    def __call__(self, pkg:str)->DataFrame:

        if pkg not in self.pacotes_busca:
            raise ValueError(f'pkg must be in {self.pacotes_busca.keys()}')

        return getattr(self,pkg)
