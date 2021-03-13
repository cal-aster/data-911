# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.imports import (
    APIRouter,
    jsonable_encoder,
    Path,
    Query,
    parser,
    timedelta,
    chain,
)
from services import city_manager, sql_executor

router = APIRouter()


@router.get("/hourly/{city_id}", summary="Return timeseries of calls on a hourly basis")
async def hourly(
    city_id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    days: int = 7,
):
    """
    Return timeseries of calls on a hourly basis
    """
    city = city_manager.describe(city_id)
    # anchor to the last day available or the date provided
    if last:
        last = parser.parse(last)
    else:
        last = parser.parse(city.get("max_date"))
    start = last - timedelta(days=days)
    # initialize the response
    start_date, end_date = start.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    list_dates = city_manager.list_dates(
        start_date, end_date, formatted_for_query=False
    )
    list_slots = [[f"{d} {h:02}:00" for h in range(24)] for d in list_dates]
    list_slots = list(chain.from_iterable(list_slots))
    list_slots = dict(zip(list_slots, [0 for _ in range(len(list_slots))]))
    # build the query and access data
    list_slots.update(
        {
            record.get("datetime"): record.get("num_calls")
            for record in sql_executor.get(
                "SELECT datetime, num_calls FROM Hourly WHERE city=? AND datetime BETWEEN ? AND ?",
                (city_id, f"{start_date} 00:00", f"{end_date} 23:00"),
            )
        }
    )

    return jsonable_encoder(
        {
            "labels": [r for r in sorted(list(list_slots.keys()))],
            "datasets": [
                {
                    "backgroundColor": "#63ACFF",
                    "borderColor": "#719DE0",
                    "borderWidth": 1,
                    "pointBackgroundColor": "#4F86D9",
                    "pointRadius": 2,
                    "data": [
                        int(list_slots.get(k)) for k in sorted(list(list_slots.keys()))
                    ],
                }
            ],
        }
    )


@router.get("/daily/{id}", summary="Return timeseries of calls on a daily basis")
async def daily(
    id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    months: int = 3,
):
    """
    Return timeseries of calls on a daily basis
    """

    # Get city name
    cty = mng.city_table(id)

    # Anchor to the last day available or the date provided
    if last:
        last = parser.parse(last)
    else:
        last = parser.parse(cty.get("max_date"))
    old = last + relativedelta(months=-months)

    # Initialize the response
    u, v = old.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    dts = mng.list_dates(u, v, query=False)
    res = dict(zip(dts, [0 for _ in range(len(dts))]))

    # Build the query and access data
    qry = f"SELECT date, num_calls FROM Daily \
            WHERE city='{id}' AND date BETWEEN '{u}' AND '{v}' \
            ORDER BY date"
    res.update({r.get("date"): r.get("num_calls") for r in mng.sql.get(qry)})

    return jsonable_encoder(
        {
            "labels": [r for r in sorted(list(res.keys()))],
            "datasets": [
                {
                    "backgroundColor": "#63ACFF",
                    "borderColor": "#719DE0",
                    "borderWidth": 1,
                    "pointBackgroundColor": "#4F86D9",
                    "pointRadius": 2,
                    "data": [int(res.get(k)) for k in sorted(list(res.keys()))],
                }
            ],
        }
    )


@router.get("/weekly/{id}", summary="Return timeseries of calls on a weekly basis")
async def weekly(
    id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    years: int = 2,
):
    """
    Return timeseries of calls on a weekly basis
    """

    # Get city name
    cty = mng.city_table(id)

    # Anchor to the last available monday
    if last:
        last = parser.parse(last)
    else:
        last = parser.parse(cty.get("max_date"))
    old = last + relativedelta(years=-years)
    last -= timedelta(days=last.weekday())
    old -= timedelta(days=old.weekday())

    # Build the query and access data
    u, v = old.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    qry = f"SELECT monday, num_calls FROM Weekly \
            WHERE city='{id}' AND monday BETWEEN '{old}' AND '{last}' \
            ORDER BY monday"
    res = {r.get("monday"): r.get("num_calls") for r in mng.sql.get(qry)}

    return jsonable_encoder(
        {
            "labels": [r for r in sorted(list(res.keys()))],
            "datasets": [
                {
                    "backgroundColor": "#63ACFF",
                    "borderColor": "#719DE0",
                    "borderWidth": 1,
                    "pointBackgroundColor": "#4F86D9",
                    "pointRadius": 2,
                    "data": [int(res.get(k)) for k in sorted(list(res.keys()))],
                }
            ],
        }
    )
