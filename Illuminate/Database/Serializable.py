class Serializable:
    def __init__(self, items=[]) -> None:
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = value

    def __delitem__(self, index):
        del self.items[index]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.items})"
