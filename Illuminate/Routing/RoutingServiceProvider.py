from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Routing.CallableDispatcher import CallableDispatcher
from Illuminate.Routing.Contracts.CallableDispatcher import (
    CallableDispatcher as CallableDispatcherContract,
)
from Illuminate.Routing.Contracts.ControllerDispatcher import (
    ControllerDispatcher as ControllerDispatcherContract,
)
from Illuminate.Routing.ControllerDispatcher import ControllerDispatcher
from Illuminate.Routing.Redirector import Redirector
from Illuminate.Routing.UrlGenerator import UrlGenerator

from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.Routing.Router import Router
from Illuminate.Http.Request import Request
from Illuminate.Http.ResponseFactory import ResponseFactory


class RoutingServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
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
        def lambda_function(app: Application):
            return Router(self.__app, self.__app.make("event"))

        self.__app.singleton("router", lambda_function)

    def __register_url_generator(self):
        def lambda_function(app: Application):
            router = self.__app.make("router")
            request = self.__app.make("request")
            config = self.__app.make("config")

            routes = router.get_routes()

            self.__app.instance("routes", routes)

            return UrlGenerator(routes, request, config["app.asset_url"])

        self.__app.singleton("url", lambda_function)

    def __register_redirector(self):
        def lambda_function(app: Application):
            return Redirector(self.__app, self.__app.make("url"))

        self.__app.singleton("redirect", lambda_function)

    def __register_http_request(self):
        def lambda_function(app: Application):
            return Request(self.__app)

        self.__app.singleton("request", lambda_function)

    def __register_http_response(self):
        def lambda_function(app: Application):
            return ResponseFactory(self.__app)

        self.__app.singleton("response", lambda_function)

    def __register_response_factory(self):
        pass

    def __register_callable_dispatcher(self):
        def lambda_function(app: Application):
            return CallableDispatcher(self.__app)

        self.__app.singleton(CallableDispatcherContract, lambda_function)

    def __register_controller_dispatcher(self):
        def lambda_function(app: Application):
            return ControllerDispatcher(self.__app)

        self.__app.singleton(ControllerDispatcherContract, lambda_function)
