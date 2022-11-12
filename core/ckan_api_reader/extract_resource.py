from typing import Union, Callable, List
from .action_api import CkanActionApiRequest
from .load_resource import ResourceDownloader
from .resource_filters import SearchByText, FilterbyFormat

from functools import partial


class ListResources:


    def __init__(self, domain:str, verify_requests:bool=False, **parser_kwargs)->None:

        self.ckan_api = CkanActionApiRequest(domain, verify_requests)

        self.pkgs = set(self.ckan_api.lst_pkgs())
        self.filter_by_format = FilterbyFormat()
        self.search_by_text = SearchByText()

        self.download_resource = ResourceDownloader(**parser_kwargs)

    def __apply_filters(self, resource: dict, filter_funcs: List[Callable])->bool:
        
        for func in filter_funcs:
            test = func(resource)
            if not test:
                return False
        
        return True

    def lst_resources(self, pkg_name: str, filter_funcs: List[Callable])->list:

        if pkg_name not in self.pkgs:
            raise ValueError(f'Pkg name {pkg_name} not in {self.pkgs}')

        return [resource for resource in self.ckan_api.lst_resources(pkg_name)
                if self.__apply_filters(resource, filter_funcs)]

    def __solve__filters(self, filter_funcs, ad_hoc_filters):

        if ad_hoc_filters:
            if type(ad_hoc_filters) is list:
                filter_funcs.extend(ad_hoc_filters)
                return
            filter_funcs.append(ad_hoc_filters)

    def lst_return(self, resources, extract, parser_params):

        if extract:
                return [self.download_resource(r, **parser_params) for r in resources]
        return resources

    def gen_return(self, resources, extract, parser_params):

        for resource in resources:

            if extract:
                yield self.download_resource(resource, **parser_params)
            else:
                yield resource

    def solve_return(self, resources:list, as_list:bool, extract:bool, parser_params:dict=None)->list:

        if as_list:
            return self.lst_return(resources, extract, parser_params)
        else:
            return self.gen_return(resources, extract, parser_params)
        
    
    def __call__(self, pkg_name: dict, format_: Union[str, list]=None, search_string: str=None, 
                    how: str=None, attr: str=None, case_sensitive: bool=None, extract:bool=False,
                    as_list:bool=False, parser_params:dict=None, ad_hoc_filters:Union[list, Callable]=None)->list:
        

        if parser_params is None:
            parser_params = {}

        text_search = partial(self.search_by_text, search_string=search_string,
                                attr=attr, case_sensitive=case_sensitive,
                                how=how)

        format_search = partial(self.filter_by_format, format_=format_)

        filter_funcs = [format_search, text_search]

        self.__solve__filters(filter_funcs, ad_hoc_filters)

        resources = self.lst_resources(pkg_name, filter_funcs)

        
        return self.solve_return(resources, as_list, extract, parser_params)
