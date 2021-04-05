# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from scrapers.imports import *

class Parser:

    def __init__(self): pass

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

    def parse(self, record, config):

        res = {k: None for k in config.keys()}

        def extract(record, source):

            if len(source) == 1: return record.get(source[0])
            else: return extract(record.get(source[0]), source[1:])

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

class CsvParser:

    def __init__(self, source_url, data_token, sql_helper=None):

        self.fmt = Parser()
        self.url = source_url
        self.tkn = data_token
        self.sql = sql_helper

    def download_csv(self, path):

        url = 'https://{}/api/views/{}/rows.csv?accessType=DOWNLOAD'
        urlretrieve(url.format(self.url, self.tkn), path)

    def browse(self, wrapper, columns, config, chunk=1000):

        lst = []
        for idx, row in enumerate(wrapper):
            if (idx % chunk == 0 and idx > 0):
                yield lst
                del lst[:]
            rec = dict(zip(columns, row))
            lst.append(self.fmt.parse(rec, config))
        yield lst

    def parse(self, path, table=None, offset=0, limit=None, chunk=250000, config=None):

        cnt = 0
        cfg = yaml.safe_load(open(config))

        with open(path) as bdy:
            fle = csv.reader(bdy)
            col = [r.strip() for r in next(fle)]
            for _ in range(offset): next(fle)
            sze = min(chunk, limit) if limit else chunk
            for lst in self.browse(fle, col, cfg, chunk=sze):
                cnt += len(lst)
                if self.sql and table:
                    self.sql.add(table, lst)
                if limit:
                    if cnt >= limit:
                        break

        return cnt

class SocrataParser:

    def __init__(self, source_url, data_token, api_token, timeout=60, sql_helper=None):

        self.fmt = Parser()
        self.url = source_url
        self.tkn = data_token
        self.api = Socrata(source_url, api_token, timeout=timeout)
        self.sql = sql_helper

    def download_csv(self, path):

        url = 'https://{}/api/views/{}/rows.csv?accessType=DOWNLOAD'
        urlretrieve(url.format(self.url, self.tkn), path)

    def size(self):

        return int(self.api.get(self.tkn, select="count(*)")[0].get('count'))

    def parse(self, table=None, offset=0, limit=10000, order=None, config=None):

        cfg = yaml.safe_load(open(config))
        res = self.api.get(self.tkn, limit=limit, order=order, offset=offset)
        prc = [self.fmt.parse(record, cfg) for record in res]

        if table:
            self.sql.add(table, prc)
            return len(res)
        else:
            return res, prc

class Tabler:

    def __init__(self, directory, sql_helper=None):

        self.drc = directory
        self.sql = sql_helper

        # Load configuration
        pth = "/".join(['scrapers', self.drc, 'description.yaml'])
        self.cfg = yaml.safe_load(open(pth))
        cty = "".join(self.cfg.get('city').strip().split(' '))
        self.tbl = f"{self.cfg.get('state').upper()}_{cty}"
        if self.cfg.get('department') != 'police':
            self.tbl += f"_{self.cfg.get('department').capitalize()}"

        # Load city ID if existing
        qry = f"SELECT id FROM Cities \
                WHERE city='{self.cfg.get('city')}' \
                  AND state='{self.cfg.get('state')}' \
                  AND department='{self.cfg.get('department')}'"
        self.cid = self.sql.unique(qry)
        if self.cid: self.cid = self.cid.get('id')

    def initialize(self):

        # Add new entry to the Cities table
        if self.cid is None: self.cid = uuid.uuid4().hex
        else: self.sql.run(f"DELETE FROM Cities WHERE id='{self.cid}'")
        self.sql.add("Cities", {
            "id": self.cid,
            "city": self.cfg.get('city'),
            "longitude": self.cfg.get('longitude'),
            "latitude": self.cfg.get('latitude'),
            "zoom": self.cfg.get('zoom'),
            "num_calls": 0,
            "state": self.cfg.get('state'),
            "state_name": self.cfg.get('state_name'),
            "timezone": self.cfg.get('timezone'),
            "population": self.cfg.get('population'),
            "department": self.cfg.get('department')
        })

        # Add the description
        qry = f"SELECT id FROM Descriptions WHERE id='{self.cid}'"
        did = self.sql.unique(qry)
        if did: self.sql.run(f"DELETE FROM Descriptions WHERE id='{self.cid}'")
        self.sql.add("Descriptions", {
            "id": self.cid,
            "api_url": self.cfg.get('api_url'),
            "attributes": json.dumps(self.cfg.get('attributes')),
            "data_token": self.cfg.get('data_token'),
            "data_url": self.cfg.get('data_url'),
            "description": self.cfg.get('description'),
            "notes": self.cfg.get('notes'),
            "primary_key": self.cfg.get('primary_key'),
            "refresh_frequency": self.cfg.get('refresh_frequency'),
            "source_url": self.cfg.get('source_url')
        })

        # Create the new table
        pth = "/".join(['scrapers', self.drc, 'schema.yaml'])
        self.sql.table_create(self.tbl, pth)

    def drop_duplicates(self, key):

        qry = f"DELETE FROM {self.tbl} WHERE ROWID NOT IN ( \
                    SELECT MIN(ROWID) FROM {self.tbl} GROUP BY {key} \
                )"
        self.sql.run(qry)
        self.update_city()

    def test_csv(self, offset):

        cfg = yaml.safe_load(open("/".join(['scrapers', self.drc, 'parser-csv.yaml'])))
        with open("/".join(['scrapers', self.drc, 'archive.csv'])) as bdy:
            fle = csv.reader(bdy)
            col = [r.strip() for r in next(fle)]
            for _ in range(offset): next(fle)
            row = next(fle)
            try: return dict(zip(col, row)), Parser().parse(dict(zip(col, row)), cfg)
            except: return dict(zip(col, row))

    def load_csv(self):

        pth = "/".join(['scrapers', self.drc, 'archive.csv'])
        # Initialize the CSV parser
        api = CsvParser(
            self.cfg.get('source_url'),
            self.cfg.get('data_token'),
            sql_helper=self.sql
        ).download_csv(pth)

    def from_csv(self):

        # Initialize the CSV parser
        api = CsvParser(
            self.cfg.get('source_url'),
            self.cfg.get('data_token'),
            sql_helper=self.sql
        )

        # Parse the CSV and add it to the DB
        api.parse(
            "/".join(['scrapers', self.drc, 'archive.csv']),
            table=self.tbl,
            chunk=100000,
            config="/".join(['scrapers', self.drc, 'parser-csv.yaml'])
        )

    def update_city(self):

        qry = f"SELECT MIN(date) as low, MAX(date) as top, COUNT(date) as cnt FROM {self.tbl}"
        sts = self.sql.unique(qry)
        qry = f"UPDATE Cities \
                SET num_calls={sts.get('cnt')}, \
                    min_date='{sts.get('low')}', \
                    max_date='{sts.get('top')}' \
                WHERE id='{self.cid}'"
        self.sql.run(qry)

    def test_api(self, offset, token, order=None):

        return SocrataParser(
            self.cfg.get('source_url'),
            self.cfg.get('data_token'),
            token
        ).parse(
            limit=1,
            order=order if order else self.cfg.get('primary_key'),
            offset=offset,
            config="/".join(['scrapers', self.drc, 'parser-api.yaml'])
        )

    def from_api(self, token, order=None, verbose=False):

        api = SocrataParser(
            self.cfg.get('source_url'),
            self.cfg.get('data_token'),
            token,
            sql_helper=self.sql
        )

        ups = 1
        while ups > 0:
            qry = f"SELECT num_calls as cnt FROM Cities WHERE id='{self.cid}'"
            ups = api.parse(
                table=self.tbl,
                order=order if order else self.cfg.get('primary_key'),
                offset=self.sql.unique(qry).get('cnt'),
                config="/".join(['scrapers', self.drc, 'parser-api.yaml'])
            )
            if verbose: print(f"# Added {ups} records")
            self.update_city()
