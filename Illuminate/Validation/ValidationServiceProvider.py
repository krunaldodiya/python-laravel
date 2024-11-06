from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Validation.Factory import Factory


class ValidationServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        self.__app.singleton("validator", lambda app: Factory(self.__app))

    def boot(self):
        pass
