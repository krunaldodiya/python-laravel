from datetime import datetime

from django.http import HttpRequest, HttpResponse

from Illuminate.Contracts.Foundation.Application import Application
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
    __middleware = []
    __middleware_groups = {}
    __middleware_aliases = {}
    __route_middleware = {}

    def __init__(self, app: Application, router: RouterContract) -> None:
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

        self.request_started_at = None

        self.__sync_middleware_to_router()

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
        self.router.middleware_priorities = self.middleware_priorities

        for key, middleware in self.middleware_groups.items():
            self.router.middleware_group(key, middleware)

        merged_middleware = {
            **self.route_middleware,
            **self.middleware_aliases,
        }

        for key, middleware in merged_middleware.items():
            self.router.alias_middleware(key, middleware)

    def handle(self, request: HttpRequest) -> HttpResponse:
        self.request_started_at = datetime.now()

        return self.send_through_router(request)

    def send_through_router(self, request: HttpRequest):
        self.__app.instance("request", request)

        self.__bootstrap()

        return (
            Pipeline(self.__app)
            .send(request)
            .through(self.middleware)
            .then(self.__dispatch_to_router())
        )

    def __dispatch_to_router(self):
        def dispatching_to_router(request):
            self.__app.instance("request", request)

            return self.router.dispatch(request)

        return dispatching_to_router

    def __bootstrap(self):
        if not self.__app.has_been_bootstrapped():
            self.__app.bootstrap_with(self.bootstrappers)

    def terminate(self, request: HttpRequest, response: HttpResponse):
        print("terminating")

    def push_middleware(self, middleware):
        if middleware not in self.middleware:
            self.middleware.append(middleware)

        return self
