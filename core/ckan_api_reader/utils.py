import requests
from inspect import isclass

class UrlBuildeR:


    def __init__(self, domain: str):

        self.domain = self.slash_ending(domain)

    def slash_ending(self, slug : str)->str:

        if not slug.endswith('/'):
            slug = slug + '/'

        return slug

    def build_params(self, params: dict)->str:
    
        params = [f'{key}={val}' for key, val in params.items()]
        
        params = '&'.join(params)
        
        return '?'+params


    def build_url(self, namespace: str, endpoint: str, **params)->str:
        
        #apenas o namespace precisa de slash, o endpoint nao
        namespace = self.slash_ending(namespace)

        url = self.domain + namespace + endpoint
        
        if params:
            params = self.build_params(params)
            url = url + params
        
        return url

    def __call__(self, namespace, endpoint, **params):

        return self.build_url(namespace, endpoint, **params)


def json_get_request(url, verify=False):

    #muitas apis do CKAN não tem SSL configurado   
    with requests.get(url, verify=verify) as r:
        if not r.status_code==200:
            raise RuntimeError(f'Erro na requisição. Status code: {r.status_code}: {r.reason}')
        return r.json()

def public_methods_set(class_)->set:

    if not isclass:
        raise ValueError('Class_ must be a class')

    method_list = [func for func in dir(class_) 
                if callable(getattr(class_, func)) and not func.startswith("__")]

    return set(method_list)
