# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

class DallasScrapper:

    TMZ = pytz.timezone(os.environ['FLASK_TIMEZONE'])
    URL = 'https://www.dallasopendata.com/resource/9fxf-t2tr.json'

    def __init__(self):

        lst = ['host', 'database', 'user', 'password', 'port', 'connect_timeout']
        self.cfg = {k: os.environ['RDS_{}'.format(k.upper())] for k in lst}
        self.cfg['port'] = int(self.cfg.get('port'))
        self.cfg['connect_timeout'] = int(self.cfg.get('connect_timeout'))

    def parse(self):

        res = json.loads(requests.get(self.URL).content)
        res = sorted(res, key=lambda x: x.get('date_time'))[::-1]

        def render(event):

            f_t = lambda x: int(datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f').timestamp())
            f_a = lambda x: [int(e) for e in x.split(',') if len(e) > 0]

            return {
                'incident': event.get('incident_number', 'undefined'),
                'class': event.get('nature_of_call', 'undefined'),
                'priority': int(event.get('priority', -1)),
                'location': event.get('location', 'undefined'),
                'area': json.dumps(f_a(event.get('reporting_area', '-1'))),
                'block': int(event.get('block', -1)),
                'date': event.get('date_time').split('T')[0],
                'time': event.get('date_time')[:-7].split('T')[-1],
                'timestamp': f_t(event.get('date_time')),
                'unit': event.get('unit_number', 'undefined'),
                'division': event.get('division', 'undefined'),
                'beat': int(event.get('beat', -1)),
                'status': event.get('status', 'undefined')
            }

        return list(map(render, res))

    def update(self):

        res = self.parse()

        tme = self.TMZ.normalize(self.TMZ.localize(datetime.now(), is_dst=True))
        log = {'emitter': 'dallas', 'timestamp': int(tme.timestamp()), 'records': len(res)}

        con = pymysql.connect(**self.cfg)
        with con.cursor() as cur:
            # Add records to RDS
            for record in res:
                val = ", ".join([r"'{}'".format(record.get(k)) for k in sorted(record.keys())])
                itm = ", ".join(sorted(record.keys()))
                qry = "INSERT INTO DallasScrapping ({}) VALUES ({})".format(itm, val)
                cur.execute(qry)
            con.commit()
            # Log the recent action
            val = ", ".join([r"'{}'".format(log.get(k)) for k in sorted(log.keys())])
            itm = ", ".join(sorted(log.keys()))
            qry = "INSERT INTO Scrappings ({}) VALUES ({})".format(itm, val)
            cur.execute(qry)
            con.commit()
        con.close()