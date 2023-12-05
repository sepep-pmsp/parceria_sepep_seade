import pandas as pd  # Add new imports to the top of `assets.py`
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    asset,
    get_dagster_logger,
)  # import the `dagster` library
from etls.utils import solve_path
from config import DATA_FOLDER
import json

from .resources import IBGE_api

@asset
def ufs(
    context: AssetExecutionContext,
    ibge_api: IBGE_api
) -> None:
    ufs = ibge_api.get_UF().json()

    context.add_output_metadata(
        metadata={
            "registros": len(ufs),
            "JSON": MetadataValue.json(ufs),
        }
    )

    file_name_path = solve_path('raw_ufs.json', DATA_FOLDER)
    with open(file_name_path, 'w') as f:
        f.write(json.dumps(ufs))

@asset(
        deps=[ufs]
)
def municipios(
    context: AssetExecutionContext,
    ibge_api: IBGE_api
) -> None:
    logger = get_dagster_logger()

    ufs_file_name_path = solve_path('raw_ufs.json', DATA_FOLDER)
    with open(ufs_file_name_path, 'r') as f:
        ufs = json.loads(f.read())

    results = []
    for uf in ufs:
        logger.info(f'Loading municipios from {uf["nome"]}')

        municipios = ibge_api.get_municipio(uf['id']).json()

        results = results + municipios

    context.add_output_metadata(
        metadata={
            "registros": len(results),
            "JSON": MetadataValue.json(results[:5]),
        }
    )

    file_name_path = solve_path('raw_municipios.json', DATA_FOLDER)
    with open(file_name_path, 'w') as f:
        f.write(json.dumps(results))