from Illuminate.Log.LogManager import LogManager

from Illuminate.Support.ServiceProvider import ServiceProvider

from Illuminate.Contracts.Foundation.Application import Application


class LogServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        self.__app.singleton("log", lambda app: LogManager(self.__app))

    def boot(self):
        pass
