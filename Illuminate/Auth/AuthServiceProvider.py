from Illuminate.Auth.Access.Gate import Gate
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.ServiceProvider import ServiceProvider


class AuthServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        self.register_access_gate()

    def boot(self):
        pass

    def register_access_gate(self):
        self.__app.singleton("gate", lambda app: Gate(self.__app))
