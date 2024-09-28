class Collection(list):
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = value

    def __delitem__(self, index):
        del self.items[index]

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return repr(self.items)

    def append(self, item):
        self.items.append(item)

    def filter(self, func):
        return Collection(list(filter(func, self.items)))

    def flatten(self):
        def _flatten(items):
            flat_list = []

            for item in items:
                if isinstance(item, list) or isinstance(item, Collection):
                    flat_list.extend(_flatten(item))
                else:
                    flat_list.append(item)

            return flat_list

        return Collection(_flatten(self.items))

    def all(self):
        return all(self.items)

    def map(self, func):
        return Collection(list(map(func, self.items)))

    def first(self, func=None):
        if func is None:
            return self.items[0] if self.items else None
        return next((item for item in self.items if func(item)), None)

    def last(self, func=None):
        if func is None:
            return self.items[-1] if self.items else None
        return next((item for item in reversed(self.items) if func(item)), None)

    def pluck(self, key):
        return Collection(
            [
                item.get(key) if isinstance(item, dict) else getattr(item, key, None)
                for item in self.items
            ]
        )

    def reduce(self, func, initial=None):
        from functools import reduce

        return reduce(func, self.items, initial)

    def sum(self, key=None):
        if key is None:
            return sum(self.items)
        return sum(
            [
                item[key] if isinstance(item, dict) else getattr(item, key, 0)
                for item in self.items
            ]
        )

    def contains(self, value):
        if callable(value):
            return any(value(item) for item in self.items)
        return value in self.items

    def each(self, func):
        for item in self.items:
            func(item)
        return self

    def is_empty(self):
        return len(self.items) == 0

    def is_not_empty(self):
        return len(self.items) > 0

    def to_list(self):
        return self.items
