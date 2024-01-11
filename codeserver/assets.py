import pandas as pd  # Add new imports to the top of `assets.py`
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    asset,
)  # import the `dagster` library
from etls import PibMunicipal
from etls.scripts.municipios import ETL as Municipios
from etls.scripts.casamentos import ETL as Casamentos

@asset
def pib_municipal(context: AssetExecutionContext) -> None:
    client = PibMunicipal()
    df = client(save_single_csv=True, return_df=True)

    n = 10

    peek = df.sample(n)

    context.add_output_metadata(
        metadata={
            'registros': df.shape[0],
            f'amostra de {n} registros': MetadataValue.md(peek.to_markdown()),
        }
    )

@asset
def municipios(context: AssetExecutionContext) -> None:
    client = Municipios()
    df = client(use_existing_file=False)

    n = 10

    peek = df.sample(n)

    context.add_output_metadata(
        metadata={
            'registros': df.shape[0],
            f'amostra de {n} registros': MetadataValue.md(peek.to_markdown()),
        }
    )

@asset
def casamentos(context: AssetExecutionContext) -> None:
    client = Casamentos()
    df = client(use_existing_file=False)

    n = 10

    peek = df.sample(n)

    context.add_output_metadata(
        metadata={
            'registros': df.shape[0],
            f'amostra de {n} registros': MetadataValue.md(peek.to_markdown()),
        }
    )
