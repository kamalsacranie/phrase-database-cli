from enum import Enum, EnumMeta
from typing import Optional, Tuple

from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    create_engine,
    inspect,
    select,
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql.schema import MetaData

import config_schema as cs
import utils


# Need to find a better way to implement column changes etc. This simply won't
# do

CONFIG = utils.get_config()


# This will not generate the ID column, that will always be done automatically
def create_cols_enum() -> EnumMeta:
    return (
        Enum(
            "ColumnsEnum",
            {key.upper(): value for key, value in CONFIG[cs.COLUMNS]},
        )
        if cs.COLUMNS in CONFIG.keys()
        else Enum("ColumnsEnum", {"PHRASE": 14, "REFERENCE": 4})
    )


cols_enum = create_cols_enum()


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

        args = [Column(col.name.lower(), String(10000)) for col in cols_enum]
        new_table = Table(
            table_name,
            self.metadata_obj,
            Column("id", Integer, primary_key=True),
            *args,
        )

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
    pass
    c = Controller("../testing.db")
    columns = c.inspector.get_columns("the prince")
    print(columns)
