# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from dateutil import parser
from datetime import timedelta
from itertools import chain
from dateutil.relativedelta import relativedelta
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Path, Query

from services import city_manager, sql_handler

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
            for record in sql_handler.get(
                "SELECT datetime, num_calls FROM Hourly WHERE city=? AND datetime BETWEEN ? AND ?",
                (city_id, f"{start_date} 00:00", f"{end_date} 23:00"),
            )
        }
    )

    return jsonable_encoder(
        {
            "labels": [date for date in sorted(list(list_slots.keys()))],
            "datasets": [
                {
                    "backgroundColor": "#63ACFF",
                    "borderColor": "#719DE0",
                    "borderWidth": 1,
                    "pointBackgroundColor": "#4F86D9",
                    "pointRadius": 2,
                    "data": [
                        int(list_slots.get(date))
                        for date in sorted(list(list_slots.keys()))
                    ],
                }
            ],
        }
    )


@router.get("/daily/{city_id}", summary="Return timeseries of calls on a daily basis")
async def daily(
    city_id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    months: int = 3,
):
    """
    Return timeseries of calls on a daily basis
    """
    city = city_manager.describe(city_id)
    # anchor to the last day available or the date provided
    if last:
        last = parser.parse(last)
    else:
        last = parser.parse(city.get("max_date"))
    start = last + relativedelta(months=-months)
    # initialize the response
    start_date, end_date = start.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    list_dates = city_manager.list_dates(
        start_date, end_date, formatted_for_query=False
    )
    list_slots = dict(zip(list_dates, [0 for _ in range(len(list_dates))]))
    # build the query and access data
    list_slots.update(
        {
            record.get("date"): record.get("num_calls")
            for record in sql_handler.get(
                "SELECT date, num_calls FROM Daily \
                WHERE city=? AND date BETWEEN ? AND ? \
                ORDER BY date",
                (city_id, start_date, end_date),
            )
        }
    )

    return jsonable_encoder(
        {
            "labels": [date for date in sorted(list(list_slots.keys()))],
            "datasets": [
                {
                    "backgroundColor": "#63ACFF",
                    "borderColor": "#719DE0",
                    "borderWidth": 1,
                    "pointBackgroundColor": "#4F86D9",
                    "pointRadius": 2,
                    "data": [
                        int(list_slots.get(date))
                        for date in sorted(list(list_slots.keys()))
                    ],
                }
            ],
        }
    )


@router.get("/weekly/{city_id}", summary="Return timeseries of calls on a weekly basis")
async def weekly(
    city_id: str = Path(..., title="Id of a given city"),
    last: str = Query(None, title="End date of the serie YYYY-MM-DD"),
    years: int = 2,
):
    """
    Return timeseries of calls on a weekly basis
    """
    city = city_manager.describe(city_id)
    # anchor to the last available monday
    if last:
        last = parser.parse(last)
    else:
        last = parser.parse(city.get("max_date"))
    start = last + relativedelta(years=-years)
    last -= timedelta(days=last.weekday())
    start -= timedelta(days=start.weekday())
    # build the query and access data
    start_date, end_date = start.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")
    list_slots = {
        record.get("monday"): record.get("num_calls")
        for record in sql_handler.get(
            "SELECT monday, num_calls FROM Weekly \
            WHERE city=? AND monday BETWEEN ? AND ? \
            ORDER BY monday",
            (city_id, start_date, end_date),
        )
    }

    return jsonable_encoder(
        {
            "labels": [date for date in sorted(list(list_slots.keys()))],
            "datasets": [
                {
                    "backgroundColor": "#63ACFF",
                    "borderColor": "#719DE0",
                    "borderWidth": 1,
                    "pointBackgroundColor": "#4F86D9",
                    "pointRadius": 2,
                    "data": [
                        int(list_slots.get(date))
                        for date in sorted(list(list_slots.keys()))
                    ],
                }
            ],
        }
    )
