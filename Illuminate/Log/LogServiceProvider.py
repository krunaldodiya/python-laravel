from typing import TYPE_CHECKING, Type

from Illuminate.Support.ServiceProvider import ServiceProvider

if TYPE_CHECKING:
    from Illuminate.Support.Foundation.Application import Application


class LogServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def register(self):
        pass

    def boot(self):
        pass
