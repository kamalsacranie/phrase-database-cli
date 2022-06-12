import os

from typing import Optional


# Different ones will need to be implemented for db_type because of format
def get_db_url(db_type: str = "sqlite", db_path: Optional[str] = None) -> str:
    """Gets our database url using some logic"""

    if db_path is not None:
        return f"{db_type}:///{db_path}"

    # config_db_path = config["database_path"]
    # if config_db_path is not None:
    #     return f"{db_type}:///{config_db_path}"

    if "XDG_DATA_HOME" in os.environ:
        return f"{db_type}:///{os.environ['XDG_DATA_HOME']}/jot/phrase.db"

    return f"{db_type}:///{os.environ['HOME']}/desktop/phrase.db"
