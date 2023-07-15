from Illuminate.Support.Facades.Facade import Facade


class App(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "app"
