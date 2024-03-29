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
from sqlalchemy.sql.base import ImmutableColumnCollection
from sqlalchemy.sql.expression import insert
from sqlalchemy.sql.schema import MetaData

from config import CONFIG
import utils


# This will not generate the ID column, that will always be done automatically
# There must be a better way to do this, surely. But I suppose, we should use
# the unix philosophy of buildign an application which is focussed on one thing
def create_cols_enum() -> EnumMeta:
    """Dynamically creating an enum based on config options"""
    return (
        Enum(
            "ColumnsEnum",
            {
                key.upper(): CONFIG.column_spec[key]
                for key in CONFIG.column_spec.keys()
            },
        )
        if CONFIG.column_spec
        else Enum("ColumnsEnum", {"PHRASE": 8, "REFERENCE": 2})
    )


class Controller:
    def __init__(self, db_path: Optional[str] = None):

        # Either coming from config, passed in as cli arg, or fallback
        self.db_url = utils.get_db_url(
            db_type=CONFIG.db_type or "sqlite", db_path=CONFIG.db_path
        )
        # Future engine as per sqlalchemy docs. creating the engine creates our
        # database if not created already
        self.engine: Engine = create_engine(self.db_url, future=True)
        self.inspector: Inspector = inspect(
            self.engine
        )  # Allows performing database schema inspection
        self.metadata_obj = MetaData(bind=self.engine)
        # If our database exists we will reflect it onto our metadata
        self.metadata_obj.reflect()

    def add_new_table(self, table_name: str) -> tuple[Optional[Table], str]:
        """Adds a new table"""
        if self.inspector.has_table(table_name):
            return None, f"{table_name} already exists in your database."

        cols_enum = create_cols_enum()
        args = [Column(col.name.lower(), String(10000)) for col in cols_enum]
        new_table = Table(
            table_name,
            self.metadata_obj,  # Links the new table to our metadata engine
            Column("id", Integer, primary_key=True),
            *args,
        )
        # Creating our new tables using the metadata engine
        self.metadata_obj.create_all()

        return new_table, f"{table_name} sucessfully created."

    def get_tables(self) -> list[Table]:
        """Returns a list of our table names"""
        return self.metadata_obj.sorted_tables

    def get_table_columns(self, table: Table) -> list[str]:
        if type(table) is str:
            table = self.get_table(table)
        table_columns: ImmutableColumnCollection = table.c
        return table_columns.keys()

    def get_table(self, table: str | Table) -> Table:
        """Reflects our table from our database"""
        if type(table) is Table:
            return table
        reflected_table = Table(
            table, self.metadata_obj, autoload_with=self.engine
        )
        return reflected_table

    def get_table_elements(self, table: Table | str) -> Tuple:
        """
        Returns all the elements in our table. Can take table or string as
        input
        """
        if type(table) is str:
            table = self.get_table(table)

        with self.engine.connect() as conn:
            elements = tuple(conn.execute(select(table)))
        return elements

    def add_table_entry(
        self, table: Table | str, phrase: str, page_number: any
    ) -> None:
        if type(table) is str:
            table = self.get_table(table)

        # We can make this dynamic by passing it through with kwargs
        stmt = insert(table).values(phrase=phrase, reference=page_number)
        with self.engine.begin() as conn:
            conn.execute(stmt)
