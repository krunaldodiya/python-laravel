from Illuminate.Support.Facades.Facade import Facade


class Config(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "config"
