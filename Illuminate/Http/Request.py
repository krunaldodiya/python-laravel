from typing import TYPE_CHECKING, Type


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
    def capture(app, server: Type["Server"]):
        request = Request(app)

        request.set_server(server)

        return request
