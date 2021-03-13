# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.utils import *

class Bastion:

    def __init__(self, control, db=None, url=None, creds=None):

        self.control = control

        if control == 'local':
            self.sql = RDS(db=db)

        if control == 'remote':
            self.url = url
            self.crd = creds
            self.authentify()

    def authentify(self):

        self.jwt = json.loads(
            requests.post(
                '/'.join([self.url, 'auth']),
                data=json.dumps(self.crd),
                headers={'Content-Type': 'application/json'}
            ).content
        )

    def run(self, query):

        if self.control == 'local':
            if isinstance(query, str): self.sql.run(query)
            else: self.sql.run_batch(query)

        if self.control == 'remote':
            requests.post(
                '/'.join([self.url, 'rds', 'run']),
                data=json.dumps({'query': query}),
                headers={
                    'Authorization': 'Bearer {}'.format(self.jwt),
                    'Content-Type': 'application/json'
                }
            )

    def get(self, query):

        if self.control == 'local':
            return self.sql.get(query)

        if self.control == 'remote':
            return json.loads(
                requests.post(
                    '/'.join([self.url, 'rds', 'get']),
                    data=json.dumps({'query': query}),
                    headers={
                        'Authorization': 'Bearer {}'.format(self.jwt),
                        'Content-Type': 'application/json'
                    }
                ).content
            )

    def unique(self, query):

        if self.control == 'local':
            return self.sql.unique(query)

        if self.control == 'remote':
            return json.loads(
                requests.post(
                    '/'.join([self.url, 'rds', 'get']) + '?unique=True',
                    data=json.dumps({'query': query}),
                    headers={
                        'Authorization': 'Bearer {}'.format(self.jwt),
                        'Content-Type': 'application/json'
                    }
                ).content
            )

    def add(self, table, item):

        if self.control == 'local':
            if isinstance(item, dict): self.sql.add(table, item)
            else: self.sql.add_batch(table, item)

        if self.control == 'remote':
            requests.post(
                '/'.join([self.url, 'rds', 'add']),
                data=json.dumps({'table': table, 'item': item}),
                headers={
                    'Authorization': 'Bearer {}'.format(self.jwt),
                    'Content-Type': 'application/json'
                }
            )

    def describe(self):

        if self.control == 'local':
            return self.sql.describe()

        if self.control == 'remote':
            return json.loads(
                requests.get(
                    '/'.join([self.url, 'rds', 'tables']),
                    headers={
                        'Authorization': 'Bearer {}'.format(self.jwt),
                        'Content-Type': 'application/json'
                    }
                ).content
            )

    def table_create(self, table, schema):

        cfg = list(yaml.safe_load(open(schema)).values())[0]

        if self.control == 'local':
            self.sql.create_table(table, cfg)

        if self.control == 'remote':
            requests.post(
                '/'.join([self.url, 'rds', 'tables']),

                data=json.dumps({'table': table, 'schema': cfg}),
                headers={
                    'Authorization': 'Bearer {}'.format(self.jwt),
                    'Content-Type': 'application/json'
                }
            )

    def table_delete(self, table):

        if self.control == 'local':
            self.sql.table_delete(table)

        if self.control == 'remote':
            requests.delete(
                '/'.join([self.url, 'rds', 'tables']),
                data=json.dumps({'table': table}),
                headers={
                    'Authorization': 'Bearer {}'.format(self.jwt),
                    'Content-Type': 'application/json'
                }
            )
