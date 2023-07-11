from core.Support.Facades.Facade import Facade


class Request(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "request"
