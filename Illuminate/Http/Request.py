from typing import TYPE_CHECKING, Type
from Illuminate.Http.ServerBag import ServerBag
from Illuminate.Support.Facades.App import App


if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class Request:
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

        self.server = None

        self.scheme = None
        self.query_string = None
        self.method = None
        self.root_path = None
        self.path = None
        self.raw_path = None

        self.headers = None

    def get(self, param):
        return self.params.get(param)

    @staticmethod
    def capture():
        request: Request = App.make("request")
        server: ServerBag = App.make("server")

        request.server = server

        request.scheme = server.scheme
        request.query_string = server.query_string
        request.method = server.method
        request.root_path = server.root_path
        request.path = server.path
        request.raw_path = server.raw_path

        request.headers = server.headers
        request.cookies = server.cookies

        return request
