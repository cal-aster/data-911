# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.helpers import *

router = APIRouter()

@router.get(
    "/hourly/{id}",
    summary="Return timeseries of calls on a hourly basis"
)
async def hourly(
    id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    days: int = 7
):
    """
        Return timeseries of calls on a hourly basis
    """

    # Get city name
    cty = mng.city_table(id)

    # Anchor to the last day available or the date provided
    if last: last = parser.parse(last)
    else: last = parser.parse(cty.get('max_date'))
    old = last - timedelta(days=days)

    # Initialize the response
    u,v = old.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    dts = mng.list_dates(u, v, query=False)
    res = [[f"{d} {h:02}:00" for h in range(24)] for d in dts]
    res = list(chain.from_iterable(res))
    res = dict(zip(res, [0 for _ in range(len(res))]))

    # Build the query and access data
    qry = f"SELECT datetime, num_calls FROM Hourly \
            WHERE city='{id}' AND datetime BETWEEN '{u} 00:00' AND '{v} 23:00'"
    res.update({
        r.get('datetime'): r.get('num_calls')
        for r in mng.sql.get(qry)
    })

    return jsonable_encoder({
        'labels': [r for r in sorted(list(res.keys()))],
        'datasets': [{
            'backgroundColor': "#63ACFF",
            'borderColor': "#719DE0",
            'borderWidth': 1,
            'pointBackgroundColor': "#4F86D9",
            'pointRadius': 2,
            'data': [int(res.get(k)) for k in sorted(list(res.keys()))]
        }]
    })

@router.get(
    "/daily/{id}",
    summary="Return timeseries of calls on a daily basis"
)
async def daily(
    id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    months: int = 3
):
    """
        Return timeseries of calls on a daily basis
    """

    # Get city name
    cty = mng.city_table(id)

    # Anchor to the last day available or the date provided
    if last: last = parser.parse(last)
    else: last = parser.parse(cty.get('max_date'))
    old = last + relativedelta(months=-months)

    # Initialize the response
    u,v = old.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    dts = mng.list_dates(u, v, query=False)
    res = dict(zip(dts, [0 for _ in range(len(dts))]))

    # Build the query and access data
    qry = f"SELECT date, num_calls FROM Daily \
            WHERE city='{id}' AND date BETWEEN '{u}' AND '{v}' \
            ORDER BY date"
    res.update({
        r.get('date'): r.get('num_calls')
        for r in mng.sql.get(qry)
    })

    return jsonable_encoder({
        'labels': [r for r in sorted(list(res.keys()))],
        'datasets': [{
            'backgroundColor': "#63ACFF",
            'borderColor': "#719DE0",
            'borderWidth': 1,
            'pointBackgroundColor': "#4F86D9",
            'pointRadius': 2,
            'data': [int(res.get(k)) for k in sorted(list(res.keys()))]
        }]
    })

@router.get(
    "/weekly/{id}",
    summary="Return timeseries of calls on a weekly basis"
)
async def weekly(
    id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    years: int = 2
):
    """
        Return timeseries of calls on a weekly basis
    """

    # Get city name
    cty = mng.city_table(id)

    # Anchor to the last available monday
    if last: last = parser.parse(last)
    else: last = parser.parse(cty.get('max_date'))
    old = last + relativedelta(years=-years)
    last -= timedelta(days=last.weekday())
    old -= timedelta(days=old.weekday())

    # Build the query and access data
    u,v = old.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    qry = f"SELECT monday, num_calls FROM Weekly \
            WHERE city='{id}' AND monday BETWEEN '{old}' AND '{last}' \
            ORDER BY monday"
    res = {
        r.get('monday'): r.get('num_calls')
        for r in mng.sql.get(qry)
    }

    return jsonable_encoder({
        'labels': [r for r in sorted(list(res.keys()))],
        'datasets': [{
            'backgroundColor': "#63ACFF",
            'borderColor': "#719DE0",
            'borderWidth': 1,
            'pointBackgroundColor': "#4F86D9",
            'pointRadius': 2,
            'data': [int(res.get(k)) for k in sorted(list(res.keys()))]
        }]
    })
