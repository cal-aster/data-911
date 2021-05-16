from fastapi import APIRouter, Path, Query
from fastapi.encoders import jsonable_encoder
from services import city_manager, sql_handler

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
    list_dates = city_manager.list_dates(start, end)
    placeholders = ", ".join(["?" for _ in list_dates])

    try:
        attributes = ["timestamp", "longitude", "latitude"]
        records = sql_handler.get(
            f"SELECT {', '.join(attributes)} FROM {city.get('table')} \
            WHERE date IN (%s) \
            ORDER BY timestamp DESC"
            % placeholders,
            list_dates,
        )
        records_number = len(records)
        records = [record for record in records if not city_manager.has_null(record)]
    except:
        records = []
        records_number = sql_handler.get_unique(
            f"SELECT COUNT(timestamp) as cnt FROM {city.get('table')} \
            WHERE date IN (%s)"
            % placeholders,
            list_dates,
        ).get("cnt")

    return jsonable_encoder(
        {
            "nRecords": records_number,
            "geojson": city_manager.build_geojson(records, "timestamp"),
        }
    )
