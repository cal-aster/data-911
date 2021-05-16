import math
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple, Union

from dateutil import parser

from services.database import SqlHandler


class Cities:
    def __init__(self, sql: SqlHandler) -> None:
        self.sql = sql
        self.spatial_columns = ["timestamp", "longitude", "latitude"]

    def describe(self, city_id: str) -> Dict:
        city_description = self.sql.get_unique(
            f"SELECT city, state, max_date, department FROM Cities WHERE id=?",
            (city_id,),
        )
        # reformat the name of the associated table
        table_name = "".join(city_description.get("city").strip().split(" "))
        table_name = f"{city_description.get('state').upper()}_{table_name}"
        if city_description.get("department") != "police":
            table_name += f"_{city_description.get('department').capitalize()}"
        # update description
        city_description.update({"table": table_name})

        return city_description

    @staticmethod
    def record_to_key(
        record: Dict, keys: List[str], intervals: List[Any]
    ) -> Union[None, List[str]]:
        date = parser.parse(f"{record.get('date')} {record.get('time', '00:00')}")
        if date < intervals[0]:
            return None
        elif date > intervals[-1]:
            return None
        else:
            gaps = [interval - date for interval in intervals]
            indexes = len([gap for gap in gaps if gap.total_seconds() < 0]) - 1
            return keys[indexes]

    @staticmethod
    def has_null(record: Dict) -> bool:
        def is_null(value: Any) -> bool:
            if value is None or value != value:
                return True
            elif isinstance(value, str):
                return (
                    value == "nan"
                    or value == "None"
                    or value == "NaN"
                    or value.strip() == ""
                )
            elif isinstance(value, float):
                return math.isnan(value)
            else:
                return False

        return any([is_null(v) for v in record.values()])

    @staticmethod
    def build_geojson(records: List[Dict], info_column: str) -> Dict:
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "id": uuid.uuid4().hex,
                        info_column: record.get(info_column),
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            record.get("longitude"),
                            record.get("latitude"),
                            0.0,
                        ],
                    },
                }
                for record in records
            ],
        }

    @staticmethod
    def list_dates(
        start: str, end: str, formatted_for_query: bool = False
    ) -> List[str]:
        if end == None:
            end = start
        start_date, end_date = parser.parse(start), parser.parse(end)
        days_difference = (end_date - start_date).days
        list_dates = [
            (start_date + timedelta(days=days)).strftime("%Y-%m-%d")
            for days in range(days_difference + 1)
        ]
        if formatted_for_query:
            list_dates = [r"'{}'".format(date) for date in list_dates]
            list_dates = f"({', '.join(list_dates)})"

        return list_dates

    @staticmethod
    def dates_to_timestamps(self, start: str, end: str) -> Tuple[int]:
        if end == None:
            end = start
        start_date, end_date = parser.parse(start), parser.parse(end)
        start_timestamp = datetime.datetime.combine(
            start_date, datetime.time.min
        ).timestamp()
        end_timestamp = datetime.datetime.combine(
            end_date, datetime.time.max
        ).timestamp()

        return int(start_timestamp), int(end_timestamp)

    def valid_dates(self, table: str) -> Dict:
        dates_extrema = self.sql.get_unique(
            f"SELECT min(date) as minDate, max(date) as maxDate FROM {table} WHERE date IS NOT NULL AND date<>'None'"
        )
        if dates_extrema is None:
            minimum, maximum = None, None
        else:
            minimum = dates_extrema.get("minDate", None)
            maximum = dates_extrema.get("maxDate", None)

        return {"minDate": minimum, "maxDate": maximum}
