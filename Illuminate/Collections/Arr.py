import math

from typing import Any, Dict, List, Union
from Illuminate.Collections.helpers import data_get
from Illuminate.Contracts.Collections.Collection import Collection as CollectionContract


class Arr:
    @classmethod
    def only(cls, items: Dict[Any, Any], keys: List[Any]):
        return {key: value for key, value in items.items() if key in keys}

    @classmethod
    def get(cls, items, key, default=None):
        return data_get(items, key, default)

    @classmethod
    def forget(cls, items, keys: List[str]):
        for key in keys:
            parts = key.split(".")
            current = items

            for part in parts[:-1]:
                if part in current:
                    current = current[part]
                else:
                    break
            else:
                if parts[-1] in current:
                    del current[parts[-1]]

    @classmethod
    def pull(cls, items, key, default=None):
        value = cls.get(items, key, default)

        cls.forget(items, key if isinstance(key, list) else [key])

        return value

    @classmethod
    def flatten(
        cls, items: Union[Dict[Any, Any], CollectionContract], depth: int = math.inf
    ) -> Dict[int, Any]:
        flattened = []

        def _flatten(current_items, current_depth):
            if isinstance(current_items, list):
                iterator = enumerate(current_items)
            elif isinstance(current_items, dict):
                iterator = current_items.items()
            elif isinstance(current_items, CollectionContract):
                iterator = current_items
            else:
                iterator = current_items

            for key, item in iterator:
                if isinstance(item, (CollectionContract, dict, list)) and (
                    depth == math.inf or current_depth < depth
                ):
                    _flatten(item, current_depth + 1)
                else:
                    flattened.append(item)

        _flatten(items, 0)

        return flattened
