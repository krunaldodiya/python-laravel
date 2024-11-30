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
from Illuminate.Routing.ResponseFactory import ResponseFactory


class RoutingServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        self._register_router()
        self._register_url_generator()
        self._register_redirector()
        self._register_http_request()
        self._register_http_response()
        self._register_response_factory()
        self._register_callable_dispatcher()
        self._register_controller_dispatcher()

    def boot(self):
        pass

    def _register_router(self):
        def lambda_function(app: Application):
            return Router(app, app.make("events"))

        self.__app.singleton("router", lambda_function)

    def _register_url_generator(self):
        def lambda_function(app: Application):
            router = app.make("router")

            config = app.make("config")

            routes = router.get_routes()

            app.instance("routes", routes)

            return UrlGenerator(
                routes,
                self.__app.rebinding("request", self._request_rebinder()),
                config["app.asset_url"],
            )

        self.__app.singleton("url", lambda_function)

    def _request_rebinder(self):
        return lambda app, request: app.make("url").set_request(request)

    def _register_redirector(self):
        def lambda_function(app: Application):
            return Redirector(app, app.make("url"))

        self.__app.singleton("redirect", lambda_function)

    def _register_http_request(self):
        def lambda_function(app: Application):
            request = Request.capture(app)

            return request

        self.__app.singleton("request", lambda_function)

    def _register_http_response(self):
        def lambda_function(app: Application):
            return ResponseFactory(app)

        self.__app.singleton("response", lambda_function)

    def _register_response_factory(self):
        pass

    def _register_callable_dispatcher(self):
        def lambda_function(app: Application):
            return CallableDispatcher(app)

        self.__app.singleton(CallableDispatcherContract, lambda_function)

    def _register_controller_dispatcher(self):
        def lambda_function(app: Application):
            return ControllerDispatcher(app)

        self.__app.singleton(ControllerDispatcherContract, lambda_function)
