import itertools
import os
import sqlite3
from typing import Callable, Dict, List, Tuple

import pymysql


class SqlHandler:

    ENVIRONMENT = os.getenv("ENV")
    MAX_COUNT_PLACEHOLDERS = 65535
    PLACEHOLDER = "%s" if os.getenv("ENV") in ["staging", "production"] else "?"

    def __init__(self) -> None:
        pass

    def connect(self, database: str = None) -> Callable:
        if self.ENVIRONMENT in ["staging", "production"]:
            self.credentials = {
                "host": os.getenv("MYSQL_HOST"),
                "database": os.getenv("MYSQL_DATABASE"),
                "user": os.getenv("MYSQL_USER"),
                "password": os.getenv("MYSQL_PASSWORD"),
                "port": int(os.getenv("MYSQL_PORT")),
                "connect_timeout": int(os.getenv("MYSQL_CONNECT_TIMEOUT")),
            }
            return pymysql.connect(**self.credentials)
        else:
            if database is not None:
                if not os.path.exists(database):
                    raise Exception("No database dump found")
                else:
                    return sqlite3.connect(database)
            elif os.getenv("SQL_DATABASE") is not None:
                if not os.path.exists(os.getenv("SQL_DATABASE")):
                    raise Exception("No database dump found")
                else:
                    return sqlite3.connect(os.getenv("SQL_DATABASE"))
            else:
                raise Exception("A database needs to be specified")

    def escape(self, query: str) -> str:
        if self.ENVIRONMENT == "dev":
            return query
        else:
            return query.replace("?", self.PLACEHOLDER)

    def run(self, query: str, values: Tuple = None) -> None:
        driver = self.connect()
        cursor = driver.cursor()
        if values:
            cursor.execute(self.escape(query), values)
        else:
            cursor.execute(self.escape(query))
        driver.commit()
        cursor.close()
        driver.close()

    def run_batch(self, queries: List[str], values: List[Tuple] = None) -> None:
        driver = self.connect()
        cursor = driver.cursor()
        for index, query in enumerate(queries):
            if values:
                cursor.execute(self.escape(query), values[index])
            else:
                cursor.execute(self.escape(query))
        driver.commit()
        cursor.close()
        driver.close()

    def get(self, query: str, values: Tuple = None) -> List[Dict]:
        driver = self.connect()
        cursor = driver.cursor()
        if values:
            cursor.execute(self.escape(query), values)
        else:
            cursor.execute(self.escape(query))
        results = cursor.fetchall()
        attributes = [attribute[0] for attribute in cursor.description]
        results = [
            {key: value for key, value in zip(attributes, result)} for result in results
        ]
        cursor.close()
        driver.close()
        return results

    def get_unique(self, query: str, values: Tuple = None) -> Dict:
        driver = self.connect()
        cursor = driver.cursor()
        if values:
            cursor.execute(self.escape(query), values)
        else:
            cursor.execute(self.escape(query))
        result = cursor.fetchone()
        if result:
            attributes = [attribute[0] for attribute in cursor.description]
            result = {key: value for key, value in zip(attributes, result)}
        cursor.close()
        driver.close()
        return result

    def add(self, table: str, item: Dict) -> None:
        attributes = sorted(list(item.keys()))
        placeholder = ",".join([self.PLACEHOLDER for _ in attributes])
        query = f"INSERT INTO {table} ({','.join(attributes)}) VALUES ({placeholder})"
        values = tuple([item.get(key) for key in attributes])
        self.run(query, values)

    def add_batch(self, table: str, items: List[Dict], batch_size: int = None) -> None:
        if len(items) > 0:
            attributes = sorted(list(items[0].keys()))
            placeholder = ", ".join([self.PLACEHOLDER for _ in attributes])
            batch_size = (
                int(self.MAX_COUNT_PLACEHOLDERS / len(items[0].keys()))
                if batch_size is None
                else batch_size
            )

            driver = self.connect()
            cursor = driver.cursor()
            for index in range(0, len(items), batch_size):
                excerpt = items[index : index + batch_size]
                if len(excerpt) > 0:
                    placeholders = ", ".join([f"({placeholder})" for _ in excerpt])
                    cursor.execute(
                        f"INSERT INTO {table} ({','.join(attributes)}) VALUES {placeholders}",
                        tuple(
                            itertools.chain.from_iterable(
                                [
                                    [item.get(key) for key in attributes]
                                    for item in excerpt
                                ]
                            )
                        ),
                    )
            driver.commit()
            cursor.close()
            driver.close()
