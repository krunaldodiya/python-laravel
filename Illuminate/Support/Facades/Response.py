from Illuminate.Support.Facades.Facade import Facade


class Response(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "response"
