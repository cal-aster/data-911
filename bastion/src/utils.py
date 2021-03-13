# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

from src.oauth import *

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

class EFS:

    def __init__(self, path="/app/efs"):

        self.drc = path

    def list(self):

        def describe(path):

            res, s_t = dict(), os.stat(path)
            res['path'] = path
            if S_ISDIR(s_t.st_mode):
                res['type'] = 'directory'
                res['items'] = {f : describe('/'.join([path, f])) for f in os.listdir(path)}
            else:
                res['type'] = 'file'
            return res

        return jsonable_encoder(describe(self.drc))

    def empty(self):

        for fle in os.listdir(self.drc):
            pth = "/".join([self.drc, fle])
            if os.path.isdir(pth): shutil.rmtree(pth, ignore_errors=True)
            else: os.remove(pth)

    def create_folder(self, path):

        os.makedirs("/".join([self.drc, path]), exist_ok=True)

    def delete_folder(self, path):

        shutil.rmtree("/".join([self.drc, path]), ignore_errors=True)

    def create_file(self, path, file):

        open("/".join([self.drc, path]), 'wb').write(file.file.read())

    def delete_file(self, path):

        os.remove("/".join([self.drc, path]))

class S3B:

    def __init__(self):

        crd = ['BCK_ACCESS_KEY_ID', 'BCK_SECRET_ACCESS_KEY']
        crd = {k.lower().replace('bck', 'aws'): os.environ[k] for k in crd}

        self._s3 = os.getenv("BCK_NAME")
        self.bck = boto3.resource("s3", os.getenv("BCK_REGION"), **crd)

    def list(self, prefix=None):

        try:
            return self.bck.meta.client.list_objects(Bucket=self._s3).get('Contents')
        except:
            return []

    def download(self, src, dst):

        self.bck.meta.client.download_file(self._s3, src, dst)

    def upload(self, src, dst):

        self.bck.meta.client.upload_file(src, self._s3, dst)

    def delete(self, uri):

        self.bck.meta.client.delete_object(Bucket=self._s3, Key=uri)
