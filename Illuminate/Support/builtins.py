from typing import Any, Dict


def array_values(data: Dict[Any, Any]):
    return [item for key, item in data]


def array_merge(main: Dict[Any, Any], other: Dict[Any, Any]):
    return {**main, **other}
