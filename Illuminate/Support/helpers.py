from Illuminate.Support.HigherOrderTapProxy import HigherOrderTapProxy


def tap(value, callback=None):
    if not callback:
        return HigherOrderTapProxy(value)

    callback(value)

    return value
