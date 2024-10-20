from Illuminate.Support.Facades.Facade import Facade


class Request(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "request"
