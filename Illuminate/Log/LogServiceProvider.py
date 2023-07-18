from typing import TYPE_CHECKING, Type
from Illuminate.Foundation.Debugger import Debugger

from Illuminate.Support.ServiceProvider import ServiceProvider

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class LogServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def register(self):
        self.__app.singleton("debug", lambda: Debugger(self.__app))

    def boot(self):
        pass
