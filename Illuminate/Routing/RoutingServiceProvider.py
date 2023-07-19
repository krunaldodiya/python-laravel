from typing import TYPE_CHECKING, Type
from Illuminate.Routing.CallableDispatcher import CallableDispatcher
from Illuminate.Routing.Contracts.CallableDispatcher import (
    CallableDispatcher as CallableDispatcherContract,
)
from Illuminate.Routing.Contracts.ControllerDispatcher import (
    ControllerDispatcher as ControllerDispatcherContract,
)
from Illuminate.Routing.ControllerDispatcher import ControllerDispatcher
from Illuminate.Routing.UrlGenerator import UrlGenerator

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
        self.__register_url_generator()
        self.__register_redirector()
        self.__register_http_request()
        self.__register_http_response()
        self.__register_response_factory()
        self.__register_callable_dispatcher()
        self.__register_controller_dispatcher()

    def boot(self):
        pass

    def __register_router(self):
        self.__app.singleton(
            "router", lambda: Router(self.__app, self.__app.make("events"))
        )

    def __register_url_generator(self):
        def generator():
            router = self.__app.make("router")
            request = self.__app.make("request")
            config = self.__app.make("config")

            routes = router.get_routes()

            self.__app.instance("routes", routes)

            return UrlGenerator(routes, request, config["app.asset_url"])

        self.__app.singleton("url", generator)

    def __register_redirector(self):
        self.__app.singleton("redirect", lambda: Router(self.__app.make("url")))

    def __register_http_request(self):
        self.__app.singleton("request", lambda: Request(self.__app))

    def __register_http_response(self):
        self.__app.singleton("response", lambda: ResponseFactory(self.__app))

    def __register_response_factory(self):
        pass

    def __register_callable_dispatcher(self):
        self.__app.singleton(
            CallableDispatcherContract, lambda: CallableDispatcher(self.__app)
        )

    def __register_controller_dispatcher(self):
        self.__app.singleton(
            ControllerDispatcherContract, lambda: ControllerDispatcher(self.__app)
        )
