from Illuminate.Support.Facades.Facade import Facade


class Event(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "events"
