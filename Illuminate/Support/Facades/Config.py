from Illuminate.Support.Facades.Facade import Facade


class Config(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "config"
