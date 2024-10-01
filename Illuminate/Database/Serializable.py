class Serializable(list):
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

    def __iter__(self):
        return iter(self.items)
