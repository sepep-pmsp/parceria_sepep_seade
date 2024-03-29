from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
    AutoMaterializePolicy,
)

from . import assets

all_assets = load_assets_from_modules(
        [assets],
        auto_materialize_policy=AutoMaterializePolicy.eager()
    )

all_assets_job = define_asset_job(
        "all_assets_job",
        selection=AssetSelection.all()
    )

all_assets_schedule = ScheduleDefinition(
    job=all_assets_job, cron_schedule="0 3 * * *"  # every day at 03:00am
)


defs = Definitions(
    assets=all_assets,
    schedules=[all_assets_schedule],
)
