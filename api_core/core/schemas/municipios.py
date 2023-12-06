from typing import List, Union, Optional
from pydantic import BaseModel, validator,root_validator

class BaseRegistro(BaseModel):

    municipio: str
    ano: str

    @validator('municipio', pre=True, always=True)
    def valid_mun(cls, v):

        return str(v)

    @validator('ano', pre=True, always=True)
    def valid_ano(cls, v):

        return int(v)


class MunicipioRegistro(BaseRegistro):

    valor : Union[float, str]


class MunicipioTudo(BaseRegistro):

    cod_municipio : int
    regiao_administrativa : str
    regiao_metropolitana : str
    valor_do_pib : float
    habitantes_do_município : Optional[float]
    nascidos_vivos : float

    @root_validator(pre=True)
    def to_float(cls, values):

        for key, v in values.items():
            if key not in ('municipio', 'ano', 'regiao_administrativa',
                           'regiao_metropolitana'):
                if type(v) is str:
                    v = v.replace(',', '.')

                    values[key] = float(v)

        return values