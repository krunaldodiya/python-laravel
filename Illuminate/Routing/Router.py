from typing import TYPE_CHECKING, Type
from Illuminate.Http.Request import Request
from Illuminate.Routing.Route import Route

from Illuminate.Routing.RouteCollection import RouteCollection


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
        self.__add_route(["GET", "HEAD"], uri, action)

    def post(self, uri, action):
        self.__add_route(["POST"], uri, action)

    def put(self, uri, action):
        self.__add_route(["PUT"], uri, action)

    def patch(self, uri, action):
        self.__add_route(["PATCH"], uri, action)

    def delete(self, uri, action):
        self.__add_route(["DELETE"], uri, action)

    def option(self, uri, action):
        self.__add_route(["OPTION"], uri, action)

    def __add_route(self, methods, uri, action):
        self.routes.add(self.__create_route(methods, uri, action))

    def __create_route(self, methods, uri, action):
        action = self.__convert_to_controller_action(action)

        return self.__new_route(methods, uri, action)

    def __new_route(self, methods, uri, action):
        return Route(methods, uri, action).set_router(self).set_application(self.__app)

    def __convert_to_controller_action(self, action):
        if isinstance(action, list):
            controller, method = action

            return {
                "uses": getattr(controller, method),
                "controller": str(controller.__class__) + "@" + method,
            }

        return {"uses": action}

    def dispatch(self, request: Request):
        self.current_request = request
        self.__dispatch_to_route(request)

    def __dispatch_to_route(self, request):
        self.__run_route(request, self.__find_route(request))

    def __find_route(self, request):
        return None

    def __run_route(self, request, route):
        return None

    def get_routes(self):
        return self.routes
