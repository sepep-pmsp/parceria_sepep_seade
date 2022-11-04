from functools import partial
from .utils import UrlBuildeR, json_get_request
from .ckan_config import DOMAIN



class CkanActionApiRequest:

    DOMAIN = DOMAIN

    def __init__(self, domain = DOMAIN, verify=False):

        build_url = UrlBuildeR(domain)
        self.build_url = partial(build_url, namespace='action')
        #geralmente as APIs do CKAN não tem certificado SSL
        self.verify=verify

    def assert_success(self, json_resp):

        assert json_resp.get('success')
    
    def __get_endpoint(self, endpoint: str, **params):

        url = self.build_url(endpoint=endpoint, **params)
        resp = json_get_request(url, verify=self.verify)

        self.assert_success(resp)

        return resp['result']

    def lst_pkgs(self)->dict:

        pkg_lst_endpoint = 'package_list'

        return self.__get_endpoint(pkg_lst_endpoint)

    def get_package(self, pkg_name: str)->dict:
    
        show_pkg_endpoint = 'package_show'
        
        return self.__get_endpoint(show_pkg_endpoint, id=pkg_name)

    def lst_resources(self, pkg_name: str)->list:

        results = self.get_package(pkg_name)

        return results['resources']
