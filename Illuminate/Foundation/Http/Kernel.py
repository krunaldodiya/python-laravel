from datetime import datetime
from typing import Optional

from Illuminate.Contracts.Foundation.Application import (
    Application as ApplicationContract,
)
from Illuminate.Foundation.Http.Events.RequestHandled import RequestHandled
from Illuminate.Support.Facades.App import App
from Illuminate.Contracts.Http.Request import Request
from Illuminate.Contracts.Http.Response import Response
from Illuminate.Contracts.Routing.Router import Router as RouterContract
from Illuminate.Foundation.Bootstrap.BootProviders import BootProviders
from Illuminate.Foundation.Bootstrap.HandleExceptions import HandleExceptions
from Illuminate.Foundation.Bootstrap.LoadConfiguration import LoadConfiguration
from Illuminate.Foundation.Bootstrap.LoadEnvironmentVariables import (
    LoadEnvironmentVariables,
)
from Illuminate.Foundation.Bootstrap.RegisterFacades import RegisterFacades
from Illuminate.Foundation.Bootstrap.RegisterProviders import RegisterProviders
from Illuminate.Foundation.Http.Middleware.HandlePrecognitiveRequests import (
    HandlePrecognitiveRequests,
)

from Illuminate.Pipeline.Pipeline import Pipeline


class Kernel:
    __middleware: list = []
    __middleware_groups: dict = {}
    __middleware_aliases: dict = {}
    __route_middleware: dict = {}

    def __init__(self, app: ApplicationContract, router: RouterContract) -> None:
        self.__app = app
        self.__router = router

        self.__middleware = self.middleware
        self.__middleware_groups = self.middleware_groups
        self.__middleware_aliases = self.middleware_aliases

        self.__bootstrappers = [
            LoadEnvironmentVariables,
            LoadConfiguration,
            HandleExceptions,
            RegisterFacades,
            RegisterProviders,
            BootProviders,
        ]

        self.__middleware_priorities = [
            HandlePrecognitiveRequests,
        ]

        self.request_started_at: Optional[datetime] = None

        self.__sync_middleware_to_router()

    @property
    def app(self):
        return self.__app

    @property
    def router(self):
        return self.__router

    @property
    def bootstrappers(self):
        return self.__bootstrappers

    @property
    def middleware_priorities(self):
        return self.__middleware_priorities

    @property
    def middleware(self):
        return self.__middleware

    @property
    def middleware_groups(self):
        return self.__middleware_groups

    @property
    def middleware_aliases(self):
        return self.__middleware_aliases

    @property
    def route_middleware(self):
        return self.__route_middleware

    def __sync_middleware_to_router(self):
        self.router.middleware_priorities(self.middleware_priorities)

        for key, middleware in self.middleware_groups.items():
            self.router.middleware_group(key, middleware)

        merged_middleware = {
            **self.route_middleware,
            **self.middleware_aliases,
        }

        for key, middleware in merged_middleware.items():
            self.router.alias_middleware(key, middleware)

    def handle(self, request: Request) -> Response:
        try:
            self.request_started_at = datetime.now()

            response = self.send_through_router(request)

            App.make("events").dispatch(RequestHandled(request, response))

            return response
        except Exception as e:
            App.make("events").dispatch(RequestHandled(request, Response()))

            raise e

    def send_through_router(self, request: Request):
        try:
            self.__app.instance("request", request)

            self.__bootstrap()

            return (
                Pipeline(self.__app)
                .send(request)
                .through(self.middleware)
                .then(lambda request: self.__dispatch_to_router(request))
            )
        except Exception as e:
            raise e

    def __dispatch_to_router(self, request):
        self.__app.instance("request", request)

        data = self.router.dispatch(request)

        return data

    def __bootstrap(self):
        try:
            if not self.__app.has_been_bootstrapped():
                self.__app.bootstrap_with(self.bootstrappers)
        except Exception as e:
            raise e

    def terminate(self, request: Request, response: Response):
        if self.__app.bound("request"):
            self.__app.forget_binding("request")

    def push_middleware(self, middleware):
        if middleware not in self.__middleware:
            self.__middleware.append(middleware)

        return self
