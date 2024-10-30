from typing import TYPE_CHECKING, Any, List, TypeVar, Union

if TYPE_CHECKING:
    from Illuminate.Collections.Collection import Collection

T = TypeVar("T")


def collect(items: T = {}, *args, **kwargs) -> "Collection[T]":
    from Illuminate.Collections.Collection import Collection

    return Collection(items, *args, **kwargs)


def value(target, *args, **kwargs):
    return target(*args, **kwargs) if callable(target) else target


def data_get(target: Any, key: Union[List[str], str] = None, default=None):
    if not key or not isinstance(key, (list, str)):
        return target

    data_keys = [key] if isinstance(key, str) else key

    for data_key in data_keys:
        keys = data_key.split(".")
        current = target

        for item in keys:
            item = item.replace("->", ".")

            if isinstance(current, dict):
                current = current.get(item, default)
            else:
                current = getattr(current, item, default)

            if current is default:
                break

        if current is not default:
            return current

    return default
