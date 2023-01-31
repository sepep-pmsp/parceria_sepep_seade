from typing import List
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


class PibRegistro(BaseRegistro):

    valor : float

    @validator('valor', pre=True, always=True)
    def to_float(cls, v):

        if type(v) is str:
            v = v.replace(',', '.')

            return float(v)

        return float(v)


class PibTudo(BaseRegistro):

    agropecuaria : float
    industria : float
    servicos_administracao_publica : float
    servicos_total_sem_adm_publica : float
    total_geral : float
    impostos : float
    pib : float
    pib_per_capita : float

    @root_validator(pre=True)
    def to_float(cls, values):

        for key, v in values.items():
            if key not in ('municipio', 'ano'):
                if type(v) is str:
                    v = v.replace(',', '.')

                    values[key] = float(v)

        return values


