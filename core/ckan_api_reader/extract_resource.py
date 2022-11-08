from typing import Union, Callable
from .action_api import CkanActionApiRequest


class ListResources:


    def __init__(self, domain, verify_requests=False):

        self.ckan_api = CkanActionApiRequest(domain, verify_requests)

        self.pkgs = set(self.ckan_api.lst_pkgs())

    def parse_resource(self, resource):
        #Aqui tem que implementar as funções de callback
        #para filtrar o recurso
        #ele deve ser capaz de receber mais de uma função
        return resource

    def lst_resources(self, pkg_name):

        if pkg_name not in self.pkgs:
            raise ValueError(f'Pkg name {pkg_name} not in {self.pkgs}')

        return [self.parse_resource(resource) for resource in 
        self.ckan_api.lst_resources(pkg_name)]