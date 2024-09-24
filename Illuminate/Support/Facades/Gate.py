from Illuminate.Support.Facades.Facade import Facade
from Illuminate.Contracts.Auth.Access.Gate import Gate as GateContract


class Gate(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return GateContract
