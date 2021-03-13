# Author:  Meryll Dindin
# Date:    January 23, 2021
# Project: CalAster

from src.imports import (
    os,
    parser,
    timedelta,
    dateutil,
    itertools,
    Socrata,
    math,
    re,
    Any,
    Union,
    Dict,
    List,
)
from services.database import Database


class Cache:
    def __init__(self, sql: Database) -> None:
        self.sql = sql

    def build_daily(self, city_id: str, table: str, start: str, end: str) -> None:
        # delete possible previous entries
        self.sql.run(
            "DELETE FROM Daily WHERE city=? AND date BETWEEN ? AND ?",
            (city_id, start, end),
        )
        # compile new daily entries
        records = self.sql.get(
            f"SELECT DISTINCT date, COUNT(date) as num_calls FROM {table} \
            WHERE date BETWEEN ? AND ? GROUP BY date ORDER BY date ASC",
            (start, end),
        )
        for record in records:
            record.update({"city": city_id})
        # write latest entries
        self.sql.add_batch("Daily", records)

    def build_weekly(self, city_id: str, start: str, end: str) -> None:
        # retrieve initial monday
        start_date = parser.parse(start)
        start_date = start_date - timedelta(days=start_date.weekday())
        # retrieve next still unreached monday
        end_date = parser.parse(end)
        end_date = end_date + timedelta(days=6 - end_date.weekday())
        # build list of weeks
        list_mondays = [
            date.strftime("%Y-%m-%d")
            for date in dateutil.rrule.rrule(
                dateutil.rrule.WEEKLY,
                byweekday=dateutil.relativedelta.MO,
                dtstart=start_date,
            ).between(start_date, end_date, inc=True)
        ]
        # redefine boundaries
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        # delete conflicting entries
        self.sql.run(
            "DELETE FROM Weekly WHERE city=? AND monday BETWEEN ? AND ?",
            (city_id, start_date, end_date),
        )
        # group daily records by weeks
        daily_records = {
            record.get("date"): record.get("num_calls")
            for record in self.sql.get(
                "SELECT DISTINCT date, num_calls FROM Daily WHERE city=? AND date BETWEEN ? AND ?",
                (city_id, start_date, end_date),
            )
        }
        weekly_records = dict(zip(list_mondays, [0 for _ in range(len(list_mondays))]))
        # iterate over the weeks
        for date, number_calls in daily_records.items():
            weekly_records[
                max([monday for monday in list_mondays if monday <= date])
            ] += number_calls
        # update Weekly table entry
        weekly_records = [
            {"monday": monday, "num_calls": num_calls, "city": city_id}
            for monday, num_calls in weekly_records.items()
        ]
        self.sql.add_batch("Weekly", weekly_records)

    def build_hourly(self, city_id: str, table: str, start: str, end: str) -> None:
        # delete conflicting entries
        self.sql.run(
            "DELETE FROM Hourly  WHERE city=? AND datetime BETWEEN ? AND ?",
            (city_id, f"{start} 00:00", f"{end} 23:59"),
        )
        # get all data over the given time period
        list_records = [
            f"{record.get('date')} {record.get('time').split(':')[0]}:00"
            for record in self.sql.get(
                f"SELECT DISTINCT date, time FROM {table} WHERE date BETWEEN ? AND ?",
                (start, end),
            )
        ]
        # iterate, group and update DB
        self.sql.add_batch(
            "Hourly",
            [
                {"datetime": group_key, "num_calls": len(list(group)), "city": city_id}
                for group_key, group in itertools.groupby(
                    sorted(list_records), key=lambda x: x
                )
            ],
        )

    def update(self, city_id: str, table: str, start: str, end: str) -> None:
        self.build_daily(city_id, table, start, end)
        self.build_weekly(city_id, start, end)
        self.build_hourly(city_id, table, start, end)


class SocrataParser:
    def __init__(
        self, source_url: str, data_token: str, api_token: str, timeout: int = 200
    ) -> None:
        self.url = source_url
        self.token = data_token
        self.client = Socrata(source_url, api_token, timeout=timeout)

    @staticmethod
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

    def to_string(self, value: Any) -> Union[str, None]:
        if self.is_null(value):
            return None
        elif not (isinstance(value, str)):
            return None
        else:
            return re.sub(" +", " ", re.sub(r"[^\w]", " ", value)).strip()

    def to_integer(self, value: Any) -> Union[int, None]:
        if self.is_null(value):
            return None
        else:
            return int(value)

    def to_float(self, value: Any) -> Union[float, None]:
        if self.is_null(value):
            return None
        else:
            return float(value)

    def to_duple(self, value: Any, index: int) -> Union[float, None]:
        if self.is_null(value):
            return None
        else:
            dup = [r.strip() for r in re.sub("[()]", "", value).split(",")]
            try:
                return [float(".".join(r.split())) for r in dup][int(index)]
            except:
                return None

    def to_regex(self, value: Any, index: int) -> Union[float, None]:
        if self.is_null(value):
            return None
        else:
            grp = re.search("\((.*?)\)", value)
            if grp is None:
                return None
            else:
                try:
                    return [float(r.strip()) for r in grp.group(1).split(",")][
                        int(index)
                    ]
                except:
                    return None

    def to_date(self, value: Any) -> Union[str, None]:
        if self.is_null(value):
            return None
        else:
            return parser.parse(value.replace(":000", " "), fuzzy=True).strftime(
                "%Y-%m-%d"
            )

    def to_timestamp(self, value: Any) -> Union[int, None]:
        if self.is_null(value):
            return None
        else:
            return int(parser.parse(value.replace(":000", " "), fuzzy=True).timestamp())

    def to_time(self, value: Any) -> Union[str, None]:
        if self.is_null(value):
            return None
        else:
            return parser.parse(value.replace(":000", " "), fuzzy=True).strftime(
                "%H:%M"
            )

    def translate(self, record: Dict, config: Dict) -> Dict:
        template = {key: None for key in config.keys()}

        def extract(record: Dict, source: List[str]) -> Any:
            if record is not None:
                if len(source) == 1:
                    return record.get(source[0])
                else:
                    return extract(record.get(source[0]), source[1:])
            else:
                return None

        for key, item in config.items():
            if item.get("type") == "string":
                template.update(
                    {
                        key: self.to_string(
                            extract(record, item.get("source").split(","))
                        )
                    }
                )
            elif item.get("type") == "integer":
                template.update(
                    {
                        key: self.to_integer(
                            extract(record, item.get("source").split(","))
                        )
                    }
                )
            elif item.get("type") == "float":
                template.update(
                    {key: self.to_float(extract(record, item.get("source").split(",")))}
                )
            elif item.get("type") == "date":
                template.update(
                    {key: self.to_date(extract(record, item.get("source").split(",")))}
                )
            elif item.get("type") == "timestamp":
                template.update(
                    {
                        key: self.to_timestamp(
                            extract(record, item.get("source").split(","))
                        )
                    }
                )
            elif item.get("type") == "time":
                template.update(
                    {key: self.to_time(extract(record, item.get("source").split(",")))}
                )
            elif item.get("type").startswith("duple"):
                template.update(
                    {
                        key: self.to_duple(
                            extract(record, item.get("source").split(",")),
                            item.get("type").split("-")[1],
                        )
                    }
                )
            elif item.get("type").startswith("regex"):
                template.update(
                    {
                        key: self.to_regex(
                            extract(record, item.get("source").split(",")),
                            item.get("type").split("-")[1],
                        )
                    }
                )

        return template

    def size(self) -> int:
        return int(self.client.get(self.token, select="count(*)")[0].get("count"))

    def parse(
        self, config: Dict, offset: int = 0, limit: int = 10000, order: str = None
    ) -> List[Dict]:
        records = self.client.get(self.token, limit=limit, order=order, offset=offset)
        return [self.translate(record, config) for record in records]


class Scraper:
    def __init__(self, city_id, sql: Database = None) -> None:
        self.sql = sql
        self.city_id = city_id
        # build city config
        self.city = self.sql.get_unique(
            "SELECT Cities.state, Cities.city, Cities.department, Cities.id, \
                Cities.num_calls, Cities.max_date, \
                Descriptions.data_token, Descriptions.primary_key, Descriptions.source_url \
            FROM Cities JOIN Descriptions ON Cities.id=Descriptions.id \
            WHERE Cities.id=?",
            (city_id,),
        )
        # reconstruct the name of table
        self.table_name = "".join(self.city.get("city").strip().split(" "))
        self.table_name = f"{self.city.get('state').upper()}_{self.tbl}"
        if self.city.get("department") != "police":
            self.table_name += f"_{self.city.get('department').capitalize()}"

    def update(self, chunk: int = 10000) -> int:
        if self.city.get("primary_key"):
            # initialize API
            api = SocrataParser(
                self.city.get("source_url"),
                self.city.get("data_token"),
                os.getenv("SOCRATA_KEY"),
            )
            # build city api configuration
            config = {
                record.get("attribute"): {
                    "source": record.get("source"),
                    "type": record.get("type"),
                }
                for record in self.sql.get(
                    "SELECT attribute, source, type FROM Scrapers WHERE city=?",
                    (self.city_id,),
                )
            }
            # initialize memory
            records, start, end, count = [None], None, None, 0
            # iterate parser up until there are no new records
            while len(records) > 0:
                records = api.parse(
                    config,
                    offset=self.city.get("num_calls") + count,
                    limit=chunk,
                    order=self.city.get("primary_key"),
                )
                records_dates = [
                    record.get("date") for record in records if record.get("date")
                ]
                count += len(records)
                if len(records_dates):
                    if start:
                        start = min(start, min(records_dates))
                    else:
                        start = min(records_dates)
                    if end:
                        end = max(end, max(records_dates))
                    else:
                        end = max(records_dates)
                if len(records):
                    self.sql.add_batch(self.table_name, records)

            if count > 0:
                self.sql.run(
                    "UPDATE Cities SET max_date=?, num_calls=? WHERE id=?",
                    (end, count + self.city.get("num_calls"), self.city_id),
                )
                # build hourly, daily and weekly cache
                Cache(self.sql).update(self.city_id, self.table_name, start, end)

            return count

        else:
            return 0
