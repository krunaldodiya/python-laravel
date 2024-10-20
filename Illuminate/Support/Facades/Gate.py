from Illuminate.Support.Facades.Facade import Facade


class Gate(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "gate"
