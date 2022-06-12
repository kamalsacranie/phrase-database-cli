from typing import Optional, Tuple
from sqlalchemy import create_engine, inspect, Integer, Column, Table, String
from sqlalchemy.sql.expression import insert, select, text
from sqlalchemy.sql.schema import MetaData

import utils

# Either coming from config, passed in as cli arg, or fallback
db_url = utils.get_db_url(db_path="../testing.db")
engine = create_engine(db_url, future=True)
inspector = inspect(engine)  # Allows performing database schema inspection
metadata_obj = MetaData(bind=engine)


def add_new_table(table_name: str) -> tuple[Optional[Table], str]:
    """Adds a new table"""
    if inspector.has_table(table_name):
        return None, f"{table_name} already exists in your database."

    new_table = Table(
        table_name,
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("phrase", String(10000)),
        Column("reference", String(1000)),
    )

    metadata_obj.create_all()

    return new_table, f"{table_name} sucessfully created."


def get_table_elements(table_name: str) -> Tuple[Tuple]:
    """Takes text input when user selects table from the tui"""
    chosen_table = Table(table_name, metadata_obj, autoload_with=engine)

    with engine.connect() as conn:
        # have to call the tuple function inside here to be able to take our
        # elements variabel outside of the function the execute returns a query
        # to the database which can only yield when it is open
        elements = tuple(conn.execute(select(chosen_table)))

    return elements


print(get_table_elements("the prince"))

# new_table, _ = add_new_table("the prince")
# for i in range(10):
#     with engine.begin() as db:
#         db.execute(
#             insert(new_table).values(
#                 phrase=f"I like this {i+1}", reference=f"On page {i+11}"
#             )
#         )
