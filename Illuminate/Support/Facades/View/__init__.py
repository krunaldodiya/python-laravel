from Illuminate.Support.Facades.Facade import Facade


class View(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "view"
