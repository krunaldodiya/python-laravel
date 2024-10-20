from Illuminate.Support.Facades.Facade import Facade


class Url(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "url"
