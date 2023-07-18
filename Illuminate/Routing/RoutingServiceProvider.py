from typing import TYPE_CHECKING, Type

from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.Routing.Router import Router
from Illuminate.Http.Request import Request
from Illuminate.Http.ResponseFactory import ResponseFactory

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class RoutingServiceProvider(ServiceProvider):
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

    def register(self):
        self.__register_router()
        self.__register_http_request()
        self.__register_http_response()

    def boot(self):
        pass

    def __register_router(self):
        self.__app.singleton("router", lambda: Router(self.__app))

    def __register_http_request(self):
        self.__app.singleton("request", lambda: Request(self.__app))

    def __register_http_response(self):
        self.__app.singleton("response", lambda: ResponseFactory(self.__app))
