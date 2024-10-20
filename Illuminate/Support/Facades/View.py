from Illuminate.Support.Facades.Facade import Facade


class View(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "view"
