from Illuminate.Support.Facades.Facade import Facade


class Event(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "event"
