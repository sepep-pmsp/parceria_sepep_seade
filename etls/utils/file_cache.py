import os
import requests
from io import BytesIO, StringIO
from typing import Union


class FileCache:
    '''Downloads a file only if it is not already saved at given file path.
    If it's saved, will only load saved file.'''

    def __init__(self, verbose=True)->None:

        self.verbose = verbose

    def load_if_exists(self, file_path:str, binary:bool)->Union[BytesIO, StringIO]:

        read = 'rb' if binary else 'r'
        reader = BytesIO if binary else StringIO

        if os.path.exists(file_path):
            with open(file_path, read) as f:
                print(f'Loading file at {file_path}')
                return reader(f.read())
            
    
    def save_file(self, file_path:str, content:Union[bytes, str], binary:bool)->None:

        print(f'Saving file at {file_path}')
        if binary:
            with open(file_path, 'wb') as f:
                f.write(content)
        else:
            with open(file_path, 'w') as f:
                f.write(content)

    def download_file(self, url:str, binary:bool)->Union[bytes, str]:

        print(f'Downloading file from {url}')
        with requests.get(url) as r:
            
            content = r.content if binary else r.text
        
        return content

    def load_and_save_file(self, url:str, file_path:str, binary=True)->Union[BytesIO, StringIO]:

        content = self.download_file(url, binary)

        self.save_file(file_path, content, binary)

        reader = BytesIO if binary else StringIO

        return reader(content)
    
    def pipeline(self, file_path:str, url:str, binary:bool)->Union[BytesIO, StringIO]:

        data = self.load_if_exists(file_path, binary) or\
            self.load_and_save_file(url, file_path, binary)
        
        return data
    
    
    def __call__(self, file_path:str, url:str, binary:bool)->Union[BytesIO, StringIO]:

        return self.pipeline(file_path, url, binary)