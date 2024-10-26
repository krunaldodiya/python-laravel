import operator

from Illuminate.Support.HigherOrderTapProxy import HigherOrderTapProxy


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


def tap(value, callback=None):
    if not callback:
        return HigherOrderTapProxy(value)

    callback(value)

    return value


def transform(value, callback=None, default=None):
    if value:
        return callback(value)

    if callable(default):
        return default(value)

    return default
