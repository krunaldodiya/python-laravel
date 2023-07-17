from Illuminate.Support.Facades.Facade import Facade


class Debug(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "debug"
