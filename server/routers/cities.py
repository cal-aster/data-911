# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.helpers import *

router = APIRouter()

@router.get(
    "",
    summary="Returns list of available cities"
)
async def cities():
    """
        Returns all available cities
    """
    col = ['city', 'id', 'max_date', 'min_date', 'num_calls', 'state_name', 'department']
    qry = f"SELECT {', '.join(col)} FROM Cities ORDER BY city"
    return jsonable_encoder(mng.sql.get(qry))

@router.get(
    "/{id}",
    summary="Returns information for a given city"
)
async def city(
    id: str = Path(..., title="Id of a given city")
):
    """
        Returns a specific city
    """
    qry = f"SELECT * FROM Cities WHERE id='{id}'"
    return jsonable_encoder(mng.sql.unique(qry))

@router.get(
    "/description/{id}",
    summary="Describe a city and its data"
)
async def description(
    id: str = Path(..., title="Id of a given city")
):
    """
        API description of a given city
    """
    qry = f"SELECT * FROM Descriptions WHERE id='{id}'"
    return jsonable_encoder(mng.sql.unique(qry))

@router.put(
    "/cache/{id}",
    summary="Overwrite the cache of a given city"
)
async def update_cache(
    id: str = Path(..., title="Id of a given city"),
    start: str = Query(..., title="Start date of update"),
    end: str = Query(..., title="End date of update"),
    limit: str = Query(None, title="Limit to a given condition")
):
    """
        Cache update of a given city
    """

    spr = Scraper(id, sql=mng.sql)

    if (limit is None) or (limit == 'daily'):
        Cache(mng.sql).build_daily(spr.cid, spr.tbl, start, end)

    if (limit is None) or (limit == 'weekly'):
        Cache(mng.sql).build_weekly(spr.cid, spr.tbl, start, end)

    if (limit is None) or (limit == 'hourly'):
        Cache(mng.sql).build_hourly(spr.cid, spr.tbl, start, end)

    return Response(status_code=status.HTTP_200_OK)

@router.put(
    "",
    summary="Fetch data and build cache"
)
async def update_city(
    chunk: int = Query(10000, title="Size of the query")
):
    """
        Scraping of all available cities
    """

    qry = f"SELECT id, state, city FROM Cities ORDER BY num_calls"

    return jsonable_encoder({
        f"{cty.get('state').upper()} | {cty.get('city').capitalize()}": Scraper(cty.get('id'), sql=mng.sql).update(chunk=chunk)
    } for cty in mng.sql.get(qry))

@router.put(
    "/{id}",
    summary="Fetch data and build cache"
)
async def update_city(
    id: str = Path(..., title="Id of a given city"),
    chunk: int = Query(10000, title="Size of the query")
):
    """
        Scraping of a given city
    """
    cnt = Scraper(id, sql=mng.sql).update(chunk=chunk)
    return jsonable_encoder({
        "records": cnt
    })
