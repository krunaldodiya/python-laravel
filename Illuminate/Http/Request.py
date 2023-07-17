from typing import TYPE_CHECKING, Type
from Illuminate.Support.Facades.App import App


if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application

from public.server import Server


class Request:
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

        self.__server = None

    @property
    def server(self):
        return self.__server

    def set_server(self, server):
        self.__server = server

    def get(self, param):
        return self.params.get(param)

    @staticmethod
    def capture():
        request: Request = App.make("request")

        server: Server = App.make("server")

        request.set_server(server)

        return request
