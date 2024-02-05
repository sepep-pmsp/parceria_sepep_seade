from fastapi import FastAPI
from v1 import pib_routes, municipio_routes, casamentos_routes


#pode colocar markdown
description = """
## API desenvolvida no âmbito da parceria entre a Coordenadoria de Avaliação e Gestão da Informação e a Fundação SEADE.
Desenvolvimento interno - time de **tecnologia de SEPEP** 🚀
"""

app = FastAPI(openapi_url="/",
    title="Parceria_SEADE_SEPEP",
    description=description,
    version="1.0.0",
    #terms_of_service="http://example.com/terms/",
    contact={
        "name": "SEPEP",
        "url": "https://www.prefeitura.sp.gov.br/cidade/secretarias/governo/planejamento/",
        "email": "hpougy@prefeitura.sp.gov.br",
    },
    license_info={
        "name": "AGPL V3.0",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
    )

    
app.include_router(pib_routes, prefix="/v1/pib")
app.include_router(municipio_routes, prefix="/v1/municipio")
app.include_router(casamentos_routes, prefix="/v1/casamentos")

