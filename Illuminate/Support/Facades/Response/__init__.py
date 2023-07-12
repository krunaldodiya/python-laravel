from Illuminate.Support.Facades.Facade import Facade


class Response(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "response"
