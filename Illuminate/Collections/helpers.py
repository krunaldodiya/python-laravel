from typing import List

from Illuminate.Helpers.Util import Util


def value(target, *args, **kwargs):
    return target(*args, **kwargs) if Util.is_function(target) else target


def data_get(target, key: List[str] | str = None, default=None):
    if not key or not isinstance(key, (list, str)):
        return target

    if isinstance(key, str):
        key = key.split(".")

    try:
        for item in key:
            item = item.replace("->", ".")

            if isinstance(target, dict):
                target = target.get(item, default)
            else:
                target = getattr(target, item, default)

            if target is default:
                break

        return target
    except (AttributeError, KeyError, TypeError):
        return default
