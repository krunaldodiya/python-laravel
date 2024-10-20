from Illuminate.Support.Facades.Facade import Facade


class App(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "app"
