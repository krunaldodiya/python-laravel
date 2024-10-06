import json
import random

from itertools import zip_longest
from functools import reduce

from Illuminate.Database.Serializable import Serializable


class Collection(Serializable):
    def __init__(self, items=None):
        self.items = items or []

    def take(self, limit):
        return self.__class__(self.items[:limit])

    def first(self, callback=None):
        if callback:
            return next((item for item in self.items if callback(item)), None)
        return self.items[0] if self.items else None

    def last(self, callback=None):
        if callback:
            return next((item for item in reversed(self.items) if callback(item)), None)
        return self.items[-1] if self.items else None

    def all(self):
        return self.items

    def avg(self, key=None):
        items = self.pluck(key).all() if key else self.items
        return sum(items) / len(items) if items else 0

    def max(self, key=None):
        items = self.pluck(key).all() if key else self.items
        return max(items) if items else None

    def chunk(self, size):
        return self.__class__(
            [self.items[i : i + size] for i in range(0, len(self.items), size)]
        )

    def collapse(self):
        return self.__class__([item for sublist in self.items for item in sublist])

    def contains(self, value):
        if callable(value):
            return any(value(item) for item in self.items)
        return value in self.items

    def count(self):
        return len(self.items)

    def diff(self, items):
        return self.__class__([item for item in self.items if item not in items])

    def each(self, callback):
        self._check_is_callable(callback)

        for item in self.items:
            callback(item)

        return self

    def every(self, callback):
        self._check_is_callable(callback)

        return all(callback(item) for item in self.items)

    def filter(self, callback):
        self._check_is_callable(callback)

        return self.__class__(list(filter(callback, self.items)))

    def flatten(self, depth=-1):
        def _flatten(items, d):
            flat_list = []
            for item in items:
                if isinstance(item, (list, Collection)) and (d != 0):
                    flat_list.extend(_flatten(item, d - 1))
                else:
                    flat_list.append(item)
            return flat_list

        return self.__class__(_flatten(self.items, depth))

    def forget(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
        return self

    def for_page(self, page, per_page):
        start = (page - 1) * per_page
        return self.__class__(self.items[start : start + per_page])

    def get(self, key, default=None):
        return self.items[key] if 0 <= key < len(self.items) else default

    def implode(self, separator):
        return separator.join(map(str, self.items))

    def is_empty(self):
        return len(self.items) == 0

    def map(self, callback):
        self._check_is_callable(callback)

        return self.__class__(list(map(callback, self.items)))

    def map_into(self, klass):
        return self.__class__([klass(item) for item in self.items])

    def merge(self, items):
        return self.__class__(self.items + list(items))

    def pluck(self, key):
        return self.__class__(
            [
                item.get(key) if isinstance(item, dict) else getattr(item, key, None)
                for item in self.items
            ]
        )

    def pop(self):
        return self.items.pop()

    def prepend(self, value):
        self.items.insert(0, value)
        return self

    def pull(self, key):
        value = self.items[key]
        del self.items[key]
        return value

    def push(self, value):
        self.items.append(value)
        return self

    def put(self, key, value):
        if isinstance(self.items, dict):
            self.items[key] = value
        return self

    def random(self, num=None):
        if num:
            return random.sample(self.items, num)
        return random.choice(self.items)

    def reduce(self, callback, initial=None):
        self._check_is_callable(callback)

        return reduce(callback, self.items, initial)

    def reject(self, callback):
        self._check_is_callable(callback)

        return self.__class__([item for item in self.items if not callback(item)])

    def reverse(self):
        return self.__class__(list(reversed(self.items)))

    def serialize(self):
        return json.dumps(self.items)

    def shift(self):
        return self.items.pop(0) if self.items else None

    def sort(self, callback=None):
        self._check_is_callable(callback)

        return self.__class__(sorted(self.items, key=callback if callback else None))

    def sum(self, key=None):
        items = self.pluck(key).all() if key else self.items
        return sum(items)

    def group_by(self, key):
        grouped = {}
        for item in self.items:
            group_key = (
                item[key] if isinstance(item, dict) else getattr(item, key, None)
            )
            grouped.setdefault(group_key, []).append(item)
        return grouped

    def transform(self, callback):
        self._check_is_callable(callback)

        self.items = [callback(item) for item in self.items]

        return self

    def unique(self, key=None):
        seen = set()
        result = []
        for item in self.items:
            val = item[key] if isinstance(item, dict) else getattr(item, key, item)
            if val not in seen:
                seen.add(val)
                result.append(item)
        return self.__class__(result)

    def where(self, key, value):
        return self.__class__(
            [
                item
                for item in self.items
                if item.get(key) == value
                if isinstance(item, dict)
            ]
        )

    def zip(self, *arrays):
        return self.__class__(list(zip_longest(self.items, *arrays)))

    def collect(self):
        return self.__class__(self.items)

    def to_list(self):
        return [item for item in self.items]

    def to_json(self):
        return json.dumps(self.items)

    def values(self):
        return self.__class__(self.items)

    def flatten(self, depth=-1):
        return self.__class__(self._flatten_items(self.items, depth))

    def _check_is_callable(self, callback):
        if not callable(callback):
            raise ValueError("The 'callback' should be a function")

    def _flatten_items(self, items, depth):
        result = []
        for item in items:
            if isinstance(item, (list, Collection)) and (depth != 0):
                result.extend(self._flatten_items(item, depth - 1))
            else:
                result.append(item)
        return result
