from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union

from api_core.core.dao import PibDao as Dao
from api_core.core.schemas import pib as schm


app = APIRouter()

def get_dao():

    dao = Dao()
    
    return dao


@app.get("/agropecuaria", response_model=List[schm.PibRegistro], tags=['Pib'])
def agropecuaria(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.agropecuaria(municipio=municipio, ano=ano)

@app.get("/industria", response_model=List[schm.PibRegistro], tags=['Pib'])
def industria(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.industria(municipio=municipio, ano=ano)

@app.get("/servicos_administracao_publica", response_model=List[schm.PibRegistro], tags=['Pib'])
def servicos_administracao_publica(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.servicos_administracao_publica(municipio=municipio, ano=ano)

@app.get("/servicos_total_sem_adm_publica", response_model=List[schm.PibRegistro], tags=['Pib'])
def servicos_total_sem_adm_publica(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.servicos_total_sem_adm_publica(municipio=municipio, ano=ano)

@app.get("/total_geral", response_model=List[schm.PibRegistro], tags=['Pib'])
def total_geral(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.total_geral(municipio=municipio, ano=ano)

@app.get("/impostos", response_model=List[schm.PibRegistro], tags=['Pib'])
def impostos(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.impostos(municipio=municipio, ano=ano)

@app.get("/pib", response_model=List[schm.PibRegistro], tags=['Pib'])
def pib(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.pib(municipio=municipio, ano=ano)

@app.get("/pib_per_capita", response_model=List[schm.PibRegistro], tags=['Pib'])
def pib(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.pib_per_capita(municipio=municipio, ano=ano)

@app.get("/pib_tudo", response_model=List[schm.PibTudo], tags=['Pib'])
def pib_all(municipio: str=None, ano: int=None, dao: Dao = Depends(get_dao)):

   return dao.pib_all(municipio=municipio, ano=ano)
