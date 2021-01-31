# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.imports import *

class RDS:

    def __init__(self, db=None):

        self.env = os.getenv("ENV", "development")

        if self.env == "development":
            self.dtb = os.getenv("SQL_DATABASE", db)

        if self.env in ["staging", "production"]:
            lst = ["host", "database", "user", "password", "port", "connect_timeout"]
            self.rds = {k: os.getenv("RDS_{}".format(k.upper())) for k in lst}
            for key in ["port", "connect_timeout"]:
                self.rds[key] = int(self.rds.get(key))

    def connect(self):

        if self.env == "development":
            return sqlite3.connect(self.dtb)

        if self.env in ["staging", "production"]:
            return pymysql.connect(**self.rds)

    ### Main SQL actions

    def run(self, query):

        con = self.connect()
        cur = con.cursor()
        try:
            cur.execute(query)
        except:
            print("# Query Failure:", query, flush=True)
        con.commit()
        cur.close()
        con.close()

    def run_batch(self, queries):

        con = self.connect()
        cur = con.cursor()
        for query in queries:
            try:
                cur.execute(query)
            except:
                print("# Query Failure:", query, flush=True)
        con.commit()
        cur.close()
        con.close()

    def unique(self, query):

        con = self.connect()
        cur = con.cursor()
        try:
            cur.execute(query)
            res = cur.fetchone()
            if not res is None:
                col = [e[0] for e in cur.description]
                res = {k: v for k, v in zip(col, res)}
        except:
            print("# Query Failure:", query, flush=True)
            res = None
        cur.close()
        con.close()

        return res

    def get(self, query):

        con = self.connect()
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        col = [e[0] for e in cur.description]
        res = [{k: v for k, v in zip(col, e)} for e in res]
        cur.close()
        con.close()

        return res

    def format_values(self, item):

        tmp = [r"'{}'".format(item.get(k).replace("'", "''"))
               if isinstance(item.get(k), str) else str(item.get(k))
               for k in sorted(item.keys())]
        return f"({', '.join(tmp)})".replace('None', 'NULL')

    def add(self, table, item):

        if item:
            val = self.format_values(item)
            col = ", ".join(sorted(item.keys()))
            qry = f"INSERT INTO {table} ({col}) VALUES {val}"
            self.run(qry)

    def add_batch(self, table, items, batch=1000):

        if len(items) > 0:
            con = self.connect()
            cur = con.cursor()
            col = ", ".join(sorted(items[0].keys()))
            for i in range(0, len(items), batch):
                val = items[i:batch+i]
                if len(val) > 0:
                    val = ", ".join([self.format_values(v) for v in val])
                    qry = f"INSERT INTO {table} ({col}) VALUES {val}"
                    cur.execute(qry)
            con.commit()
            cur.close()
            con.close()

    ### Table CRUD actions

    def describe(self):

        if self.env == 'development':
            return {
                r.get('name'): {
                    v.get('name'): v.get('type') + f"{' NOT NULL' if v.get('notnull') else ''}"
                    for v in self.get(f"PRAGMA table_info([{r.get('name')}])")
                } for r in self.get("SELECT name FROM sqlite_master WHERE type='table'")
            }

        if self.env in ["staging", "production"]:
            nme = f"Tables_in_{os.getenv('RDS_DATABASE')}"
            return {
                r.get(nme): {
                    v.get('Field'): v.get('Type').upper() + f"{' NOT NULL' if v.get('Null') == 'NO' else ''}"
                    for v in self.get(f"DESCRIBE {r.get(nme)}")
                } for r in self.get("SHOW TABLES")
            }

    def create_table(self, table, config):

        self.delete_table(table)
        qry = " ".join(['CREATE', 'TABLE', table])
        prm = ", ".join([" ".join([k,v]) for k,v in config.items()])
        self.run(" ".join([qry, "({})".format(prm)]))

    def delete_table(self, table):

        self.run("DROP TABLE IF EXISTS {}".format(table))
