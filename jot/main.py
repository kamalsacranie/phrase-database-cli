import os
import re
import yaml
import inspect


def config_opt(func):
    """A lovely little decorator function which lets us check if we have a
    config option using some syntactical sugar"""

    @property
    def inner(self):
        if func.__name__ not in self._CONFIG.keys():
            return None
        return func(self)

    return inner


class Config:
    def __init__(self, config_file_path: str) -> None:
        self._CONFIG = self._load_config(config_file_path) or {}

    # Rationale for making all of these cleaning functions into properties is
    # that they will only be run when they are called and thus an instantiation
    # of the class does not make all the cleaning process run
    @config_opt
    def db_path(self) -> str:
        # Probably going to need to change this to get the absolute path from
        # where the config is situated.
        """Returns either the expanded absolute path specified in the config or
        returns the absolute path if given"""
        config_path = self._CONFIG["db_path"]
        path_root_re = re.compile(r"^\/")
        if not re.match(path_root_re, config_path):
            return os.path.abspath(config_path)
        # Strip off trailing slash if exists
        return re.sub(r"\/$", "", config_path)

    @config_opt
    def db_type(self) -> str:
        """Returns what the user set for db_type"""
        return self._CONFIG[
            "db_type"
        ]  # Surely theres a way to do this dynamically

    @config_opt
    def column_spec(self) -> str:
        """Returns what the user set for db_type"""
        return self._CONFIG[
            "column_spec"
        ]  # Surely theres a way to do this dynamically

    def _load_config(self, cfg_path: str) -> dict[str, str]:
        """Parses yaml config file
        :returns: config dictionary
        """
        with open(cfg_path, "r") as f:
            return yaml.safe_load(f)


CONFIG = Config("../config.yaml")

if __name__ == "__main__":
    pass
