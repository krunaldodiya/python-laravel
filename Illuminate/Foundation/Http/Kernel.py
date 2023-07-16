from typing import TYPE_CHECKING, Type
from Illuminate.Foundation.Bootstrap.BootProviders import BootProviders
from Illuminate.Foundation.Http.Middleware.HandlePrecognitiveRequests import (
    HandlePrecognitiveRequests,
)

from Illuminate.Http.Request import Request
from Illuminate.Http.Response import Response


if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application
    from Illuminate.Routing.Router import Router


class Kernel:
    def __init__(self, app: Type["Application"], router: Type["Router"]) -> None:
        self.__app = app
        self.__router = router

        self.middleware = {}
        self.middleware_groups = {}
        self.route_middleware = {}
        self.middleware_aliases = {}

        self.__bootstrapers = [
            BootProviders,
        ]

        self.__middleware_priorities = [
            HandlePrecognitiveRequests,
        ]

        self.__sync_middleware_to_router()

    @property
    def bootstrapers(self):
        return self.__bootstrapers

    @property
    def middleware_priorities(self):
        return self.__middleware_priorities

    def __sync_middleware_to_router(self):
        self.__router.middleware_priorities = self.__middleware_priorities

        for key, middleware in self.middleware_groups.items():
            self.__router.middleware_group(key, middleware)

        merged_middleware = {
            **self.route_middleware,
            **self.middleware_aliases,
        }

        for key, middleware in merged_middleware.items():
            self.__router.alias_middleware(key, middleware)

    def handle(self, request: Request) -> Response:
        return self.__app.make("response")

    def terminate(self, request: Request, response: Response):
        print("terminating request")
