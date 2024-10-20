from Illuminate.Support.Facades.Facade import Facade


class Log(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "log"
