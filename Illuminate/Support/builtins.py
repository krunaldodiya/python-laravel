import time

from functools import lru_cache
from importlib import import_module
from typing import Any, Dict, List, Union


def use_module(ref: str):
    items = ref.split(".")

    class_name = items.pop()

    module_path = ".".join(items)

    module = import_module(module_path)

    return getattr(module, class_name)


def array_values(data: Dict[Any, Any]):
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return [item for key, item in data.items()]
    else:
        return data


from typing import Any, Dict, List, Union


def array_merge(
    main: Union[Dict[Any, Any], List[Any]],
    other: Union[Dict[Any, Any], List[Any]],
) -> Union[Dict[Any, Any], List[Any]]:
    if isinstance(main, list) and isinstance(other, list):
        return main + other
    elif isinstance(main, dict) and isinstance(other, dict):
        return {**main, **other}
    else:
        raise Exception(
            "Both arguments must be of the same type (either both lists or both dictionaries)"
        )


def array_merge_recursive(
    main: Union[Dict[Any, Any], List[Any]],
    other: Union[Dict[Any, Any], List[Any]],
) -> Union[Dict[Any, Any], List[Any]]:
    if isinstance(main, list) and isinstance(other, list):
        return main + other
    elif isinstance(main, dict) and isinstance(other, dict):
        merged = main.copy()

        for key, value in other.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = array_merge_recursive(merged[key], value)
            elif (
                key in merged
                and isinstance(merged[key], list)
                and isinstance(value, list)
            ):
                merged[key] = merged[key] if not value else merged[key] + value
            elif key in merged and value is None:
                merged[key] = merged[key]
            else:
                merged[key] = value

        return merged
    else:
        raise Exception(
            "Both arguments must be of the same type (either both lists or both dictionaries)"
        )


def timed_lru_cache(seconds: int, maxsize: int = 128):
    """Decorator that caches results for a specified time (in seconds)."""

    def wrapper(func):
        func._cache_time = time.time()

        @lru_cache(maxsize=maxsize)
        def cached_func(*args, **kwargs):
            return func(*args, **kwargs)

        def wrapped_func(*args, **kwargs):
            if time.time() - func._cache_time > seconds:
                cached_func.cache_clear()
                func._cache_time = time.time()

            return cached_func(*args, **kwargs)

        return wrapped_func

    return wrapper
