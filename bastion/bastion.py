import argparse
import json
import os
from typing import List, Optional, Union

import requests
import yaml
from dotenv import load_dotenv

dotenv_path = os.path.join(".devops", ".env.development")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

from src.services.rds import RdsHandler


class Bastion:
    def __init__(self, mode: str, host: str = None, credentials: dict = None):
        self.mode = mode
        if self.mode == "local":
            self.sql = RdsHandler()
        elif self.mode == "remote":
            self.host = host
            self.credentials = credentials
            self.login()

    def login(self):
        jwt_token = json.loads(
            requests.post(
                f"{self.host}/oauth",
                data=json.dumps(self.credentials),
                headers={"Content-Type": "application/json"},
            ).content
        )
        self.headers = {
            "Authorization": "Bearer {}".format(jwt_token),
            "Content-Type": "application/json",
        }

    def run(self, query: str):
        if self.mode == "local":
            if isinstance(query, str):
                self.sql.run(query)
            elif isinstance(query, list):
                self.sql.run_batch(query)
        elif self.mode == "remote":
            requests.post(
                f"{self.host}/rds/run",
                data=json.dumps({"query": query}),
                headers=self.headers,
            )

    def run_batch(self, queries: List[str]):
        if self.mode == "local":
            self.sql.run_batch(queries)
        elif self.mode == "remote":
            requests.post(
                f"{self.host}/rds/run-batch",
                data=json.dumps({"queries": queries}),
                headers=self.headers,
            )

    def get(self, query: str, cast: bool = True) -> List[dict]:
        if self.mode == "local":
            return self.sql.get(query, cast=cast)
        elif self.mode == "remote":
            return json.loads(
                requests.post(
                    f"{self.host}/rds/get",
                    data=json.dumps({"query": query}),
                    headers=self.headers,
                ).content
            )

    def get_unique(self, query: str) -> Optional[dict]:
        if self.mode == "local":
            return self.sql.get_unique(query)
        elif self.mode == "remote":
            return json.loads(
                requests.post(
                    f"{self.host}/rds/get-unique",
                    data=json.dumps({"query": query}),
                    headers=self.headers,
                ).content
            )

    def add(self, table: str, item: dict):
        if self.mode == "local":
            self.sql.add(table, item)
        elif self.mode == "remote":
            requests.post(
                f"{self.host}/rds/add",
                data=json.dumps({"table": table, "item": item}),
                headers=self.headers,
            )

    def add_batch(self, table: str, items: List[dict]):
        if self.mode == "local":
            self.sql.add_batch(table, items)
        elif self.mode == "remote":
            requests.post(
                f"{self.host}/rds/add-batch",
                data=json.dumps({"table": table, "items": items}),
                headers=self.headers,
            )

    def describe(self):
        if self.mode == "local":
            description = f"Tables_in_{os.getenv('RDS_DATABASE')}"
            return {
                table.get(description): {
                    attribute.get("Field"): attribute.get("Type").upper()
                    + f"{' NOT NULL' if attribute.get('Null') == 'NO' else ''}"
                    for attribute in self.get(f"DESCRIBE {table.get(description)}")
                }
                for table in self.get("SHOW TABLES")
            }

        elif self.mode == "remote":
            return json.loads(
                requests.get(f"{self.host}/rds/describe", headers=self.headers).content
            )

    def drop_constraints(self, config: dict[str, Union[str, list]]):
        table_name = config.get("name")
        constraints = config.get("constraints")

        if constraints is not None:
            for constraint in constraints:
                try:
                    self.sql.run(
                        f"ALTER TABLE {table_name} \
                        DROP CONSTRAINT {constraint.split(' ')[0]}"
                    )
                except:
                    pass

    @staticmethod
    def delete_table_query(config: dict[str, Union[str, list]]):
        return f"DROP TABLE IF EXISTS {config.get('name')}"

    @staticmethod
    def create_table_query(config: dict[str, Union[str, list]]):
        table_name = config.get("name")
        attributes = config.get("columns")
        query = f"CREATE TABLE {table_name} ({', '.join(attributes)})"
        return query

    @staticmethod
    def constrain_table_index(config: dict[str, Union[str, list]]):
        table_name = config.get("name")
        constraint = config.get("index")

        if constraint is not None:
            return f"ALTER TABLE {table_name} ADD {constraint}"

        return None

    @staticmethod
    def constrain_table_keys(config: dict[str, Union[str, list]]):
        table_name = config.get("name")
        constraints = config.get("constraints")

        if constraints is not None:
            return [
                f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint}"
                for constraint in constraints
            ]

        return []

    def initialize(
        self,
        path_tables: str = "./schemas/tables",
        path_fillers: str = "./schemas/fillers",
    ):
        queries = []
        constraints = []
        print("> Build table schemas ...")
        print("> Initialize indexing ...")
        for schema in os.listdir(path_tables):
            schema_config = yaml.safe_load(open(f"{path_tables}/{schema}"))
            self.drop_constraints(schema_config)
            queries.append(self.delete_table_query(schema_config))
            queries.append(self.create_table_query(schema_config))
            queries.append(self.constrain_table_index(schema_config))
            constraints += self.constrain_table_keys(schema_config)

        self.sql.run_batch(list(filter(lambda x: x is not None, queries + constraints)))

        filler_tables = []
        filler_items = []
        print("> Prepopulate database ...")
        for schema in os.listdir(path_tables):
            if os.path.exists(f"{path_fillers}/{schema}"):
                schema_config = yaml.safe_load(open(f"{path_tables}/{schema}"))
                schema_filler = yaml.safe_load(open(f"{path_fillers}/{schema}"))
                filler_tables += [
                    schema_config.get("name") for _ in range(len(schema_filler))
                ]
                filler_items += schema_filler

        self.sql.add_as_run_batch(filler_tables, filler_items, forced_constraints=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bastion shell scripts")
    parser.add_argument("-s", "--script", type=str, help="Script tag")
    args = parser.parse_args()
    sql = Bastion("local")

    if args.script == "init":
        sql.initialize()

    elif args.script == "describe":
        print(json.dumps(sql.describe(), indent=4))
