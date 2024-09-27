from Illuminate.Support.Facades.Facade import Facade


class Gate(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "gate"
