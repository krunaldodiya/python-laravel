from Illuminate.Support.Facades.Facade import Facade


class Log(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "log"
