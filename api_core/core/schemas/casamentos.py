from pydantic import BaseModel, validator,root_validator

class Casamentos(BaseModel):

    nome_municipio_destino: str
    ano : float
    lon_destino : float
    lat_destino : float
    total_casamentos : int