from pathlib import Path
from typing import Any, Dict, Self


class Repository:
    def __init__(
        self, items: Dict[str, Any] = {}, config_path: str | Path = ""
    ) -> None:
        self.__items: Dict[str, Any] = items

        self.__config_path: Path = (
            config_path if isinstance(config_path, Path) else Path(config_path)
        )

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    @property
    def path(self):
        return str(self.__config_path)

    def has(self, key):
        return self.get(key) is not None

    def get(self, key, default=None):
        config = self.__items
        parts = key.split(".")

        for part in parts:
            if isinstance(config, dict) and part in config:
                config = config[part]
            else:
                return default

        return config

    def get_all(self):
        return self.__items

    def set(self, key, value) -> Self:
        keys = key.split(".")
        config = self.__items

        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}

            config = config[k]

        config[keys[-1]] = value

        return self

    def get_files(self):
        items = []

        if self.__config_path.exists():
            items = [
                file
                for file in self.__config_path.iterdir()
                if file.is_file() and file.suffix == ".py"
            ]

        return items
