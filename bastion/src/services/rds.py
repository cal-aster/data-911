import itertools
import os
import re
from typing import List, Optional

import pymysql


class RdsHandler:
    PLACEHOLDER = "%s"
    RDS_CONNECT_TIMEOUT = 10
    MAX_COUNT_PLACEHOLDERS = 65535

    def connect(self):
        self.credentials = {
            "host": os.getenv("RDS_HOST"),
            "database": os.getenv("RDS_DATABASE"),
            "user": os.getenv("RDS_USER"),
            "password": os.getenv("RDS_PASSWORD"),
            "port": int(os.getenv("RDS_PORT")),
            "connect_timeout": self.RDS_CONNECT_TIMEOUT,
        }
        return pymysql.connect(**self.credentials)

    @staticmethod
    def escape(name: str):
        return f"`{name}`"

    @staticmethod
    def flatten(values: tuple):
        return tuple(
            itertools.chain(
                *(value if isinstance(value, list) else (value,) for value in values)
            )
        )

    def format(self, query: str, values: tuple = None):
        placeholder_indexes = [
            occurence.start(0) for occurence in re.finditer("\?", query)
        ]
        if len(placeholder_indexes) > 0 and values is not None:
            offset = 0
            for placeholder_index, value in zip(placeholder_indexes, values):
                if isinstance(value, list):
                    placeholder = f"({', '.join([self.PLACEHOLDER for _ in value])})"
                    query = (
                        query[: placeholder_index + offset]
                        + placeholder
                        + query[placeholder_index + offset + 1 :]
                    )
                    offset = offset + len(placeholder) - 1

        return query.replace("?", self.PLACEHOLDER)

    def run(self, query: str, values: tuple = None):
        driver = self.connect()
        cursor = driver.cursor()

        if values is not None:
            cursor.execute(self.format(query, values=values), self.flatten(values))
        else:
            cursor.execute(query)

        driver.commit()
        cursor.close()
        driver.close()

    def run_batch(self, queries: List[str], values: List[tuple] = None):
        driver = self.connect()
        cursor = driver.cursor()

        if values is None:
            values = [None for _ in range(len(queries))]
        for query, value in zip(queries, values):
            if value is not None:
                cursor.execute(
                    self.format(query, values=value),
                    self.flatten(value),
                )
            else:
                cursor.execute(query)

        driver.commit()
        cursor.close()
        driver.close()

    def get(self, query: str, values: tuple = None, cast: bool = True) -> List[dict]:
        driver = self.connect()
        cursor = driver.cursor()

        if values is not None:
            cursor.execute(self.format(query, values=values), self.flatten(values))
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        if cast:
            attributes = [attribute[0] for attribute in cursor.description]
            results = [
                {key: value for key, value in zip(attributes, result)}
                for result in results
            ]

        cursor.close()
        driver.close()
        return results

    def get_unique(self, query: str, values: tuple = None) -> Optional[dict]:
        driver = self.connect()
        cursor = driver.cursor()

        if values is not None:
            cursor.execute(self.format(query, values=values), self.flatten(values))
        else:
            cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            attributes = [attribute[0] for attribute in cursor.description]
            result = {key: value for key, value in zip(attributes, result)}

        cursor.close()
        driver.close()
        return result

    def add(self, table: str, item: dict, strict: bool = True):
        attributes = sorted(list(item.keys()))
        columns = [self.escape(attribute) for attribute in attributes]
        placeholder = ",".join([self.PLACEHOLDER for _ in attributes])
        self.run(
            f"INSERT {'' if strict else 'IGNORE'}\
            INTO {table} ({','.join(columns)}) \
            VALUES ({placeholder})",
            tuple([item.get(key) for key in attributes]),
        )

    def add_batch(
        self,
        table: str,
        items: List[dict],
        strict: bool = True,
        batch_size: int = None,
    ):
        if len(items) == 0:
            return

        attributes = sorted(list(items[0].keys()))
        columns = [self.escape(attribute) for attribute in attributes]
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
                    f"INSERT {'' if strict else 'IGNORE'} \
                    INTO {table} ({','.join(columns)}) \
                    VALUES {placeholders}",
                    tuple(
                        itertools.chain.from_iterable(
                            [[item.get(key) for key in attributes] for item in excerpt]
                        )
                    ),
                )

        driver.commit()
        cursor.close()
        driver.close()

    def add_as_run_batch(
        self,
        tables: List[str],
        items: List[dict],
        strict: bool = True,
        forced_constraints: bool = False,
    ):
        if len(items) == 0 or len(tables) != len(items):
            return

        driver = self.connect()
        cursor = driver.cursor()

        list_queries = []
        list_values = []
        for table, item in zip(tables, items):
            attributes = sorted(list(item.keys()))
            columns = [self.escape(attribute) for attribute in attributes]
            placeholder = ",".join([self.PLACEHOLDER for _ in attributes])
            list_queries.append(
                f"INSERT {'' if strict else 'IGNORE'} \
                INTO {table} ({','.join(columns)}) \
                VALUES ({placeholder})"
            )
            list_values.append(tuple([item.get(key) for key in attributes]))

        if forced_constraints:
            self.run_batch(
                [
                    "SET FOREIGN_KEY_CHECKS = 0",
                    *list_queries,
                    "SET FOREIGN_KEY_CHECKS = 1",
                ],
                [None, *list_values, None],
            )
        else:
            self.run_batch(list_queries, list_values)

        driver.commit()
        cursor.close()
        driver.close()
