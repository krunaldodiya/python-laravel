from Illuminate.Support.Facades.Facade import Facade


class Url(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "url"
