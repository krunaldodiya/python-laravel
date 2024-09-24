from Illuminate.Auth.Access.Gate import Gate
from Illuminate.Contracts.Auth.Access.Gate import Gate as GateContract
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.ServiceProvider import ServiceProvider


class AuthServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        self.register_gate_access()

    def register_gate_access(self):
        self.__app.singleton(GateContract, lambda app: Gate(self.__app))
