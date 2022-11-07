
from typing import Union, Callable

class FilterbyFormat:


    def is_format(resource: dict, format_: str)->bool:
    
        r_format = resource.get('format')
        
        if r_format is None:
            return False
        
        r_format = r_format.lower().strip()
        format_ = format_.lower().strip()
        
        return r_format == format_
    
    
    def format_in(resource: dict, formats : list)->bool:
        
        formats = set(f.lower().strip() for f in formats)
        
        if r_format is None:
            return False
        
        r_format = r_format.lower().strip()
        
        return r_format in formats

    def solve_format(self, format_ : Union[str, list])->Callable:
        
        if type(format_) is str:
            return self.is_format
        
        return self.format_in

    def __call__(self, resource_list: list, format_: Union[str, list]):

        filter_funct = self.solve_format(format_)

        return [res for res in resource_list if filter_funct(res, format_)]