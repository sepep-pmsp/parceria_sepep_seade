
from typing import Union, Callable, List
import re
from re import Pattern as RePattern
from .utils import public_methods_set

class FilterbyFormat:


    def is_format(self, resource: dict, format_: str)->bool:
    
        r_format = resource.get('format')
        
        if r_format is None:
            return False
        
        r_format = r_format.lower().strip()
        format_ = format_.lower().strip()
        
        return r_format == format_
    
    
    def format_in(self, resource: dict, formats : list)->bool:
        
        formats = set(f.lower().strip() for f in formats)
        
        r_format = resource.get('format')
        
        if r_format is None:
            return False
        
        r_format = r_format.lower().strip()
        
        return r_format in formats

    def solve_format(self, format_ : Union[str, list])->Callable:
        
        if type(format_) is str:
            return self.is_format
        
        return self.format_in

    def __call__(self, resource: dict, format_: Union[str, list])->bool:

        if format_ is None:
            return True

        filter_funct = self.solve_format(format_)

        return filter_funct(resource, format_)


class SearchByText:

    allowed_attrs = {'description', 'name'}

    def __init__(self, case_sensitive = False):

        self.case_sensitive = case_sensitive
        #all public methods must implement a search operation
        self.search_operations = public_methods_set(self)

    def __extract_txt_val(self, resource: dict, attr: str)->str:

        if attr not in self.allowed_attrs:
            raise ValueError(f'Attr must be in {self.allowed_attrs}')

        return resource.get(attr, '')
    
    def __lower_txt(self, search_text: str, txt_val: str, case_sensitive = None)->List[str]:


        case_sensitive = case_sensitive or self.case_sensitive
        if not case_sensitive:
            search_text = search_text.lower()
            txt_val = txt_val.lower()

        return search_text.strip(), txt_val.strip()

    def __compile_re(self, string: str)->bool:

        if isinstance(string, RePattern):
            return string
        
        return re.compile(string)


    def equals(self, txt_val: str, search_text: str, case_sensitive = None)->bool:

        search_text, txt_val = self.__lower_txt(search_text, txt_val, 
                                                case_sensitive)

        return search_text == txt_val

    def contains(self, txt_val: str, search_text: str, case_sensitive = None)->bool:

        search_text, txt_val = self.__lower_txt(search_text, txt_val, 
                                                case_sensitive)

        return search_text in txt_val

    def regex(self, txt_val: str, search_patt: RePattern,
                    case_sensitive = None)->bool:

        if not isinstance(search_patt, RePattern):
            raise ValueError('Search pattern must be pre-compiled')

        #should never change re pattern casing otherwise regex will change
        _, txt_val = self.__lower_txt('', txt_val, case_sensitive)
        
        if re.search(search_patt, txt_val):
            return True
        return False

    def __call__(self, resource: dict, search_string: Union[str, None], attr:str=None, 
                     how:str=None, case_sensitive:bool=None)->bool:

        if search_string is None:
            return True

        how = how or 'equals'
        filter_func = getattr(self, how)

        if attr is None:
            attr ='description'
        txt_val = self.__extract_txt_val(resource, attr)

        if how == 'regex':
            search_string = self.__compile_re(search_string)
        
        return filter_func(txt_val, search_string, case_sensitive)


        

    


