import requests
from io import StringIO, BytesIO
import pandas as pd
from bs4 import BeautifulSoup
import json

class ResourceParser:

    def __init__(self, csv_params = None, xl_params=None, html_params=None,
                txt_params=None, json_params=None):

        self.params = {
                    'csv' : csv_params or {},
                    'xl' : xl_params or {},
                    'html' : html_params or {},
                    'txt' : txt_params or {},
                    'json' : json_params or {}
                    }

    def parse_csv(self, response, **params):

        csv_params = self.params['csv'].copy()
        csv_params.update(params)

        response = response.text
        io = StringIO(response)

        return pd.read_csv(io, **csv_params)

    def parse_xl(self, response, **params):

        xl_params = self.params['xl'].copy()
        xl_params.update(params)

        response = response.content
        io = BytesIO(response)

        return pd.read_excel(io, **xl_params)

    def parse_json(self, response, **params):

        json_params = self.params['json'].copy()
        json_params.update(params)

        return json.loads(response, **json_params)

    def return_content(self, response, **params):

        return response.content

    def parse_response(self, response, mime_type, **params):


        parse_funcs = {
            'json' : self.parse_json,
            'csv' : self.parse_csv,
            'xls' : self.parse_xl,
            'xlsx' : self.parse_xl
        }

        parse_func = parse_funcs.get(mime_type, self.return_content)

        return parse_func(response, **params)

    def __call__(self, response, mime_type, **params):

        return self.parse_response(response, mime_type, **params)

class ResourceDownloader:

    def __init__(self, csv_params= None, xl_params= None, html_params=None, 
                txt_params=None, json_params=None, verify_ssl=False, verbose=False):

        #geralmente as APIs do CKAN não tem certificado ssl
        self.verify = verify_ssl
        self.verbose = verbose

        self.parse_response = ResourceParser(csv_params, xl_params, html_params,
                txt_params, json_params)


    def get_mime_type(self, resource):

        mime_type = resource.get('format', '')
        mime_type = mime_type.lower().strip()

        return mime_type

    def download_resource(self, resource, verify=False, **params):
        
        verify = verify or self.verify
        url = resource.get('url')
        if url:

            mime_type = self.get_mime_type(resource)
            if self.verbose: 
                print(f'Reading {mime_type} file.')

            with requests.get(url, verify=self.verify) as r:
                return self.parse_response(r, mime_type, **params)

    def __call__(self, resource, **params):

        return self.download_resource(resource, **params)
