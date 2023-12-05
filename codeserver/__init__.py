from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)

from . import assets
from .resources import IBGE_api

all_assets = load_assets_from_modules([assets])

municipios_job = define_asset_job("municipios_job", selection=AssetSelection.all())

municipios_schedule = ScheduleDefinition(
    job=municipios_job, cron_schedule="*/10 * * * *"  # every 10 minutes
)

ibge_api = IBGE_api()

defs = Definitions(
    assets=all_assets,
    schedules=[municipios_schedule],
    resources={
        'ibge_api': ibge_api
    },
)
