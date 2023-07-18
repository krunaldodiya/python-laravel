from typing import TYPE_CHECKING, Type

from Illuminate.Routing.RouteCollection import RouteCollection
from Illuminate.Support.Facades.Debug import Debug


if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application
    from Illuminate.Events.Dispatcher import Dispatcher


class Router:
    def __init__(self, app: Type["Application"], events: Type["Dispatcher"]) -> None:
        self.__app = app
        self.__events = events

        self.routes = RouteCollection()
        self.current = None
        self.current_request = None

        self.middleware = {}
        self.middleware_groups = {}
        self.middleware_priorities = {}

    def middleware_group(self, key, middleware):
        self.middleware_groups[key] = middleware
        return self

    def alias_middleware(self, key, middleware):
        self.middleware[key] = middleware
        return self

    def get(self, uri, action):
        self.add_route(["GET", "HEAD"], uri, action)

    def post(self, route, handler):
        self.add_route(route, handler, "POST")

    def add_route(self, methods, uri, action):
        self.routes.add(self.create_route(methods, uri, action))

    def dispatch(self, request):
        Debug.dd(request)
