from enum import Enum
from typing import Optional, Tuple

from sqlalchemy import Column, Integer, String, Table, create_engine, inspect
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql.schema import MetaData

import utils


CONFIG = utils.get_config()


# This will not generate the ID column, that will always be done automatically
def create_cols_enum():
    return (
        Enum(
            "Columns", {key.lower(): value for key, value in CONFIG["columns"]}
        )
        if "columns" in CONFIG.keys()
        else Enum("Columns", {"PHRASE": 5, "REFERENCE": 4})
    )

    #     if "columns" in [key.lower for key in CONFIG.keys()]:
    #         create_cols_enum(CONFIG["columns"])
    #
    # Enum("Columns", {"ID": 1, "bar": 24})


class Controller:
    def __init__(self, db_path: Optional[str] = None):

        # Either coming from config, passed in as cli arg, or fallback
        self.db_url = utils.get_db_url(db_path=db_path)
        self.engine: Engine = create_engine(self.db_url, future=True)
        self.inspector: Inspector = inspect(
            self.engine
        )  # Allows performing database schema inspection
        self.metadata_obj = MetaData(bind=self.engine)

    def add_new_table(self, table_name: str) -> tuple[Optional[Table], str]:
        """Adds a new table"""
        if self.inspector.has_table(table_name):
            return None, f"{table_name} already exists in your database."

        new_table = Table(
            table_name,
            self.metadata_obj,
            Column("id", Integer, primary_key=True, info={"width": "1"}),
            Column("phrase", String(10000), info={"width": "6"}),
            Column(
                "reference", String(1000), info={"width": "3"}, comment="test"
            ),
        )

        new_table.info

        self.metadata_obj.create_all()

        return new_table, f"{table_name} sucessfully created."

    def get_table(self, table_name: str) -> Table:
        "Reflects our table from our database"
        reflexted_table = Table(
            table_name, self.metadata_obj, autoload_with=self.engine
        )
        return reflexted_table

    def get_table_elements(self, table: Table | str) -> Tuple[Tuple]:
        """
        Returns all the elements in our table. Can take table or string as
        input
        """
        if type(table) is str:
            table = self.get_table(table)

        with self.engine.connect() as conn:
            # have to call the tuple function inside here to be able to take
            # our elements variabel outside of the function the execute returns
            # a query to the database which can only yield when it is open
            elements = tuple(conn.execute(select(table)))

        return elements


if __name__ == "__main__":
    c = Controller("../testing.db")
    columns = c.inspector.get_columns("the prince")
    print(columns)
