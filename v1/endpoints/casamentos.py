from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union

from api_core.core.dao import CasamentosDAO as Dao
from api_core.core.schemas import casamentos as schm


app = APIRouter()

def get_dao():

    dao = Dao()
    
    return dao


@app.get("/casamentos", response_model=schm.Casamentos, tags=['Casamentos'])
def casamentos(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

    try:
        return dao.casamentos_sp_com_mun(municipio=municipio, ano=ano)
    except ValueError as e:
        raise HTTPException(404, str(e))