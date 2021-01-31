# Author:  Meryll Dindin
# Date:    January 23, 2021
# Project: CalAster

from src.models import *

class Cache:

    def __init__(self, sql):

        self.sql = sql

    def build_daily(self, city, table, start, end):

        # Delete possible previous entries
        qry = f"DELETE FROM Daily \
                WHERE city='{city}' AND date BETWEEN '{start}' AND '{end}'"
        self.sql.run(qry)
        # Compile new entries
        qry = f"SELECT DISTINCT date, COUNT(date) as num_calls \
                FROM {table} \
                WHERE date BETWEEN '{start}' AND '{end}' \
                GROUP BY date ORDER BY date ASC"
        lst = self.sql.get(qry)
        for itm in lst: itm.update({"city": city})
        # Write latest entries
        self.sql.add_batch('Daily', lst)

    def build_weekly(self, city, table, start, end):

        # Delete conflicting entries
        m_n = parser.parse(start)
        m_n = m_n - timedelta(days=m_n.weekday())
        m_n = m_n.strftime("%Y-%m-%d")
        qry = f"DELETE FROM Weekly \
                WHERE city='{city}' AND monday BETWEEN '{m_n}' AND '{end}'"
        self.sql.run(qry)
        # Build the list of mondays
        qry = f"SELECT MIN(date) AS min_date, MAX(date) AS max_date \
                FROM Daily WHERE city='{city}' \
                 AND date BETWEEN '{start}' AND '{end}'"
        dts = self.sql.unique(qry)
        m_n = parser.parse(dts.get('min_date'))
        m_n = m_n - timedelta(days=m_n.weekday())
        m_x = parser.parse(dts.get('max_date'))
        dts = [
            r.strftime("%Y-%m-%d") for r in dateutil.rrule.rrule(
                dateutil.rrule.WEEKLY,
                byweekday=dateutil.relativedelta.MO,
                dtstart=m_n
            ).between(m_n, m_x, inc=True)
        ]
        # Group by weeks
        qry = f"SELECT DISTINCT date, num_calls FROM Daily \
                WHERE city='{city}' \
                  AND date BETWEEN '{start}' AND '{end}'"
        num = {r.get('date'): r.get('num_calls') for r in self.sql.get(qry)}
        res = dict(zip(dts, [0 for _ in range(len(dts))]))
        for dte, num in num.items():
            res[max([d for d in dts if d <= dte])] += num
        # Update Weekly table entry
        lst = [
            {
                "monday": key,
                "num_calls": value,
                "city": city
            }
            for key, value in res.items()
        ]
        self.sql.add_batch('Weekly', lst)

    def build_hourly(self, city, table, start, end):

        # Delete conflicting entries
        qry = f"DELETE FROM Hourly \
                WHERE city='{city}' \
                  AND datetime BETWEEN '{start} 00:00' AND '{end} 23:59'"
        self.sql.run(qry)
        # Get all data over the week
        qry = f"SELECT DISTINCT date, time FROM {table} \
                WHERE date BETWEEN '{start}' AND '{end}'"
        lst = [
            f"{r.get('date')} {r.get('time').split(':')[0]}:00"
            for r in self.sql.get(qry)
        ]
        # Iterate, group, update DB
        lst = [
            {
                "datetime": key,
                "num_calls": len(list(grp)),
                "city": city
            }
            for key, grp in itertools.groupby(sorted(lst), key=lambda x: x)
        ]
        self.sql.add_batch('Hourly', lst)

    def update(self, city, table, start, end):

        self.build_daily(city, table, start, end)
        self.build_weekly(city, table, start, end)
        self.build_hourly(city, table, start, end)

class SocrataParser:

    def __init__(self, source_url, data_token, api_token, timeout=160):

        self.url = source_url
        self.tkn = data_token
        self.api = Socrata(source_url, api_token, timeout=timeout)

    @staticmethod
    def is_null(value):

        if value is None or value != value:
            return True
        elif isinstance(value, str):
            return value == 'nan' or value == 'None' or value == 'NaN' or value.strip() == ''
        elif isinstance(value, float):
            return isnan(value)
        else:
            return False

    def to_string(self, value):

        if self.is_null(value):
            return None
        elif not(isinstance(value, str)):
            return None
        else:
            return re.sub(' +', ' ', re.sub(r'[^\w]', ' ', value)).strip()

    def to_integer(self, value):

        if self.is_null(value):
            return None
        else:
            return int(value)

    def to_float(self, value):

        if self.is_null(value):
            return None
        else:
            return float(value)

    def to_duple(self, value, index):

        if self.is_null(value):
            return None
        else:
            dup = [r.strip() for r in re.sub('[()]', '', value).split(',')]
            try: return [float('.'.join(r.split())) for r in dup][int(index)]
            except: return None

    def to_regex(self, value, index):

        if self.is_null(value):
            return None
        else:
            grp = re.search("\((.*?)\)", value)
            if grp is None:
                return None
            else:
                try: return [float(r.strip()) for r in grp.group(1).split(',')][int(index)]
                except: return None

    def to_date(self, value):

        if self.is_null(value):
            return None
        else:
            return parser.parse(value.replace(':000', ' '), fuzzy=True).strftime("%Y-%m-%d")

    def to_timestamp(self, value):

        if self.is_null(value):
            return None
        else:
            return int(parser.parse(value.replace(':000', ' '), fuzzy=True).timestamp())

    def to_time(self, value):

        if self.is_null(value):
            return None
        else:
            return parser.parse(value.replace(':000', ' '), fuzzy=True).strftime("%H:%M")

    def translate(self, record, config):

        res = {k: None for k in config.keys()}

        def extract(record, source):

            if record:
                if len(source) == 1: return record.get(source[0])
                else: return extract(record.get(source[0]), source[1:])
            else:
                return None

        for key, itm in config.items():
            if itm.get('type') == 'string':
                res.update({
                    key: self.to_string(extract(record, itm.get("source").split(',')))
                })
            elif itm.get('type') == 'integer':
                res.update({
                    key: self.to_integer(extract(record, itm.get("source").split(',')))
                })
            elif itm.get('type') == 'float':
                res.update({
                    key: self.to_float(extract(record, itm.get("source").split(',')))
                })
            elif itm.get('type') == 'date':
                res.update({
                    key: self.to_date(extract(record, itm.get("source").split(',')))
                })
            elif itm.get('type') == 'timestamp':
                res.update({
                    key: self.to_timestamp(extract(record, itm.get("source").split(',')))
                })
            elif itm.get('type') == 'time':
                res.update({
                    key: self.to_time(extract(record, itm.get("source").split(',')))
                })
            elif itm.get('type').startswith('duple'):
                res.update({
                    key: self.to_duple(extract(record, itm.get("source").split(',')), itm.get('type').split('-')[1])
                })
            elif itm.get('type').startswith('regex'):
                res.update({
                    key: self.to_regex(extract(record, itm.get("source").split(',')), itm.get('type').split('-')[1])
                })

        return res

    def size(self):

        return int(self.api.get(self.tkn, select="count(*)")[0].get('count'))

    def parse(self, config, offset=0, limit=10000, order=None):

        res = self.api.get(self.tkn, limit=limit, order=order, offset=offset)

        return [self.translate(record, config) for record in res]

class Scraper:

    def __init__(self, city, sql=None):

        self.sql = sql
        self.cid = city

        # Build city config
        qry = f"SELECT Cities.state, Cities.city, Cities.department, Cities.id, \
                       Cities.num_calls, Cities.max_date, \
                       Descriptions.data_token, Descriptions.primary_key, Descriptions.source_url \
                FROM Cities JOIN Descriptions ON Cities.id=Descriptions.id \
                WHERE Cities.id='{self.cid}'"
        self.cty = self.sql.unique(qry)
        # Reconstruct name of table
        self.tbl = "".join(self.cty.get('city').strip().split(' '))
        self.tbl = f"{self.cty.get('state').upper()}_{self.tbl}"
        if self.cty.get('department') != 'police':
            self.tbl += f"_{self.cty.get('department').capitalize()}"

    def update(self, chunk=10000):

        if self.cty.get('primary_key'):
            # Initialize API
            api = SocrataParser(
                self.cty.get("source_url"),
                self.cty.get("data_token"),
                os.getenv("SOCRATA_KEY")
            )
            # Build city api configuration
            qry = f"SELECT attribute, source, type \
                    FROM Scrapers WHERE city='{self.cid}'"
            cfg = {
                r.get('attribute'): {
                    "source": r.get('source'),
                    "type": r.get('type')
                } for r in self.sql.get(qry)
            }

            # Initialize memory
            rec, start, end, count = [None], None, None, 0
            # Iterate parser up until no new records
            while len(rec) > 0:
                rec = api.parse(
                    cfg,
                    offset=self.cty.get('num_calls') + count,
                    limit=chunk,
                    order=self.cty.get('primary_key')
                )
                tmp = [r.get('date') for r in rec if r.get('date')]
                count += len(rec)
                if len(tmp):
                    # Overwrite memory
                    if start: start = min(start, min(tmp))
                    else: start = min(tmp)
                    if end: end = max(end, max(tmp))
                    else: end = max(tmp)
                if len(rec):
                    # Add to DB
                    self.sql.add_batch(self.tbl, rec)

            if count > 0:
                # Update general city configuration
                qry = f"UPDATE Cities \
                        SET max_date='{end}', num_calls={count + self.cty.get('num_calls')} \
                        WHERE id='{self.cid}'"
                self.sql.run(qry)
                # Build hourly, daily and weekly cache
                Cache(self.sql).update(self.cid, self.tbl, start, end)

            return count

        else:
            return 0
