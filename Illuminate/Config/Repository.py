from pathlib import Path
from typing import Any, Dict


class Repository:
    def __init__(self, items: Dict[str, Any] = {}, config_path: Path = "") -> None:
        self.__items: Dict[str, Any] = items
        self.__config_path: Path = config_path

    @property
    def path(self):
        return str(self.__config_path)

    def has(self, key):
        return False if not self.get(key) else True

    def get(self, key, default=None):
        return self.__items.get(key, default)

    def get_all(self):
        return self.__items

    def set(self, key, value):
        self.__items[key] = value

    def get_files(self):
        return [
            file
            for file in self.__config_path.iterdir()
            if file.is_file() and file.suffix == ".py"
        ]
