from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union

from api_core.core.dao import MunicipiosDAO as Dao
from api_core.core.schemas import municipios as schm


app = APIRouter()

def get_dao():

    dao = Dao()
    
    return dao


@app.get("/regiao_administrativa", response_model=schm.MunicipioRegistro, tags=['Dados Municipais'])
def regiao_administrativa(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):
   
   try:
    return dao.regiao_administrativa(municipio=municipio, ano=ano)
   except ValueError as e:
        raise HTTPException(404, str(e))

@app.get("/regiao_metropolitana", response_model=schm.MunicipioRegistro, tags=['Dados Municipais'])
def regiao_metropolitana(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):
    
    try:
       return dao.regiao_metropolitana(municipio=municipio, ano=ano)
    except ValueError as e:
        raise HTTPException(404, str(e))


@app.get("/pib", response_model=schm.MunicipioRegistro, tags=['Dados Municipais'])
def pib(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

    try:
        return dao.pib(municipio=municipio, ano=ano)
    except ValueError as e:
        raise HTTPException(404, str(e))

@app.get("/habitantes", response_model=schm.MunicipioRegistro, tags=['Dados Municipais'])
def habitantes(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

    try:
        return dao.habitantes(municipio=municipio, ano=ano)
    except ValueError as e:
        raise HTTPException(404, str(e))

@app.get("/nascidos_vivos", response_model=schm.MunicipioRegistro, tags=['Dados Municipais'])
def nascidos_vivos(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

    try:
        return dao.nascidos_vivos(municipio=municipio, ano=ano)
    except ValueError as e:
        raise HTTPException(404, str(e))

@app.get("/all_data", response_model=schm.MunicipioTudo, tags=['Dados Municipais'])
def all_data(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):
    
    try:
        return dao.dados_municipio_all(municipio=municipio, ano=ano)
    except ValueError as e:
        raise HTTPException(404, str(e))