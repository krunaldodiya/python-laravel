import inspect
import operator

from typing import Any, Callable, Optional, TypeVar
from Illuminate.Support.HigherOrderTapProxy import HigherOrderTapProxy


T = TypeVar("T")
R = TypeVar("R")


def safe_eval_compare(key, oper, value):
    compare_ops = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
    }

    if oper in compare_ops:
        return compare_ops[oper](key, value)
    else:
        raise ValueError("Invalid operator")


def tap(value: T, callback: Optional[Callable[[T], R]] = None):
    if not callback:
        return HigherOrderTapProxy(value)

    callback(value)

    return value


def transform(
    value: T,
    callback: Optional[Callable[[T], R]] = None,
    default: Optional[Callable[[T], R]] = None,
):
    if value:
        return callback(value)

    if callable(default):
        return default(value)

    return default


def with_(value: T, callback: Optional[Callable[[T], R]] = None) -> T:
    if not callback:
        return value

    return callback(value)


def is_class(obj: Any):
    return inspect.isclass(obj)


def is_class_instance(obj: Any):
    if is_class(obj):
        return False

    return isinstance(obj, obj.__class__)
