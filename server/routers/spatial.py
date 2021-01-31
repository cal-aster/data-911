# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.helpers import *

router = APIRouter()

@router.get(
    "/{id}",
    summary="Returns geojson of spatio-temporal records"
)
async def raw_spatial_records(
    start: str = Query(..., title="Start date request"),
    end: str = Query(None, title="End date request"),
    id: str = Path(..., title="Id of a given city")
):
    """
        Returns a list of spatio-temporal records of
        calls for service from the corresponding table (city) that took place
        from the corresponding start date to end date.
    """

    # Get the name of the table
    qry = f"SELECT city, state, department FROM Cities WHERE id='{id}'"
    cty = mng.sql.unique(qry)
    nme = "".join(cty.get('city').strip().split(' '))
    nme = f"{cty.get('state').upper()}_{nme}"
    if cty.get('department') != 'police':
        nme += f"_{cty.get('department').capitalize()}"

    # Retrieve the calls
    dts = mng.list_dates(start, end, query=True)

    try:
        col = ['timestamp', 'longitude', 'latitude']
        qry = f"SELECT {', '.join(col)} FROM {nme} \
                WHERE date in {dts} \
                ORDER BY timestamp DESC"
        lst = mng.sql.get(qry)
        tot = len(lst)
        # Filter the calls that can be visualized
        lst = [r for r in lst if not mng.has_null(r)]
    except:
        qry = f"SELECT COUNT(timestamp) as cnt FROM {nme} \
                WHERE date in {dts}"
        lst = []
        tot = mng.sql.unique(qry).get('cnt')

    return jsonable_encoder({
        "nRecords": tot,
        "geojson": mng.build_geojson(lst, 'timestamp')
    })
