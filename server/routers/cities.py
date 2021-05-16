from fastapi import APIRouter, Path, Query, Response, status
from fastapi.encoders import jsonable_encoder
from services import sql_handler
from services.scraper import Cache, Scraper

router = APIRouter()


@router.get("", summary="Returns list of available cities")
async def cities():
    """
    Returns all available cities
    """
    attributes = [
        "city",
        "id",
        "max_date",
        "min_date",
        "num_calls",
        "state_name",
        "department",
    ]
    return jsonable_encoder(
        sql_handler.get(f"SELECT {', '.join(attributes)} FROM Cities ORDER BY city")
    )


@router.get("/{city_id}", summary="Returns information for a given city")
async def city(city_id: str = Path(..., title="Id of a given city")):
    """
    Returns a specific city
    """
    return jsonable_encoder(
        sql_handler.get_unique("SELECT * FROM Cities WHERE id=?", (city_id,))
    )


@router.get("/description/{city_id}", summary="Describe a city and its data")
async def description(city_id: str = Path(..., title="Id of a given city")):
    """
    API description of a given city
    """
    return jsonable_encoder(
        sql_handler.get_unique("SELECT * FROM Descriptions WHERE id=?", (city_id,))
    )


@router.put("/cache/{city_id}", summary="Overwrite the cache of a given city")
async def update_cache(
    city_id: str = Path(..., title="Id of a given city"),
    start: str = Query(..., title="Start date of update"),
    end: str = Query(..., title="End date of update"),
    limit: str = Query(None, title="Limit to a given condition"),
):
    """
    Cache update of a given city
    """
    scraper = Scraper(city_id, sql=sql_handler)
    if (limit is None) or (limit == "daily"):
        Cache(sql_handler).build_daily(scraper.city_id, scraper.table_name, start, end)
    if (limit is None) or (limit == "weekly"):
        Cache(sql_handler).build_weekly(scraper.city_id, start, end)
    if (limit is None) or (limit == "hourly"):
        Cache(sql_handler).build_hourly(scraper.city_id, scraper.table_name, start, end)

    return Response(status_code=status.HTTP_200_OK)


@router.put("", summary="Fetch data and build cache")
async def update_city(chunk: int = Query(10000, title="Size of the query")):
    """
    Scraping of all available cities
    """
    return jsonable_encoder(
        {
            f"{city.get('state').upper()} | {city.get('city').capitalize()}": Scraper(
                city.get("id"), sql=sql_handler
            ).update(chunk=chunk)
        }
        for city in sql_handler.get(
            "SELECT id, state, city FROM Cities ORDER BY num_calls"
        )
    )


@router.put("/{city_id}", summary="Fetch data and build cache")
async def update_city(
    city_id: str = Path(..., title="Id of a given city"),
    chunk: int = Query(10000, title="Size of the query"),
):
    """
    Scraping of a given city
    """
    return jsonable_encoder(
        {"records": Scraper(city_id, sql=sql_handler).update(chunk=chunk)}
    )
