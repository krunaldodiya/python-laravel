from core.Support.Facades.Facade import Facade


class Route(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "router"
