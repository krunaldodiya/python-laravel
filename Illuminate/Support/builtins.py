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


def array_merge(
    main: Union[Dict[Any, Any], List[Any]],
    other: Union[Dict[Any, Any], List[Any]],
):
    if isinstance(main, list) and isinstance(other, list):
        return main + other
    elif isinstance(main, dict) and isinstance(other, dict):
        return {**main, **other}
    else:
        raise Exception("invalid items")


def timed_lru_cache(seconds: int, maxsize: int = 128):
    """Decorator that caches results for a specified time (in seconds)."""

    def wrapper(func):
        # Initialize the cache expiration time
        func._cache_time = time.time()

        # Apply lru_cache with the specified maxsize
        @lru_cache(maxsize=maxsize)
        def cached_func(*args, **kwargs):
            return func(*args, **kwargs)

        def wrapped_func(*args, **kwargs):
            # If the cache has expired, clear it and reset the time
            if time.time() - func._cache_time > seconds:
                cached_func.cache_clear()
                func._cache_time = time.time()

            return cached_func(*args, **kwargs)

        return wrapped_func

    return wrapper
