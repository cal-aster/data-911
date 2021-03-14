# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.imports import APIRouter, Query, Path, jsonable_encoder
from services import sql_executor, city_manager

router = APIRouter()


@router.get("/{city_id}", summary="Returns geojson of spatio-temporal records")
async def raw_spatial_records(
    start: str = Query(..., title="Start date request"),
    end: str = Query(None, title="End date request"),
    city_id: str = Path(..., title="Id of a given city"),
):
    """
    Returns a list of spatio-temporal records of
    calls for service from the corresponding table (city) that took place
    from the corresponding start date to end date.
    """
    city = city_manager.describe(city_id)
    list_dates = city_manager.list_dates(start, end, formatted_for_query=True)

    try:
        attributes = ["timestamp", "longitude", "latitude"]
        records = sql_executor.get(
            f"SELECT {', '.join(attributes)} FROM {city.get('table')} \
            WHERE date in ? \
            ORDER BY timestamp DESC",
            (list_dates,),
        )
        records_number = len(records)
        records = [record for record in records if not city_manager.has_null(record)]
    except:
        records = []
        records_number = sql_executor.get_unique(
            f"SELECT COUNT(timestamp) as cnt FROM {city.get('table')} \
            WHERE date in ?",
            (list_dates,),
        ).get("cnt")

    return jsonable_encoder(
        {
            "nRecords": records_number,
            "geojson": city_manager.build_geojson(records, "timestamp"),
        }
    )
