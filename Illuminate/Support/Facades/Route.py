from Illuminate.Support.Facades.Facade import Facade


class Route(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "router"
