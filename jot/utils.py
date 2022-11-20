import os
import yaml

from typing import Optional


# Different ones will need to be implemented for db_type because of format
def get_db_url(db_type: str = "sqlite", db_path: Optional[str] = None) -> str:
    """Concatenates our `db_path` with our `db_type` to generate the correct
    `sqlalchemy` string"""

    if db_path is not None:
        return f"{db_type}:///{db_path}/jot.db"

    if "XDG_DATA_HOME" in os.environ:
        return f"{db_type}:///{os.environ['XDG_DATA_HOME']}/jot/jot.db"

    return f"{db_type}:///{os.environ['HOME']}/desktop/jot.db"
