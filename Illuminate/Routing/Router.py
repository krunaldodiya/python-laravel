from typing import Any, Dict, List
from Illuminate.Contracts.Events import Dispatcher
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Http.Request import Request
from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Routing.Redirector import Redirector
from Illuminate.Routing.Route import Route

from Illuminate.Routing.RouteCollection import RouteCollection
from Illuminate.View.ViewFactory import ViewFactory


class RouteNotFound(Exception):
    pass


class Router:
    def __init__(self, app: Application, events: Dispatcher) -> None:
        self.__app = app

        self.__events = events

        self.routes = RouteCollection()

        self.current = None

        self.current_request = None

        self.__middleware = {}

        self.__middleware_groups = {}

        self.__middleware_priorities = {}

        self.__registered_paths = []

        self.__attributes = self.__get_default_attributes()

        self.__allowed_attributes = self.__attributes.keys()

    def get_middleware(self):
        return self.__middleware

    def get_middleware_groups(self):
        return self.__middleware_groups

    def get_middleware_priorities(self):
        return self.__middleware_priorities

    def middleware(self, middleware: List[Any]):
        self.__set_middleware(middleware)

        return self

    def middleware_group(self, key, middleware):
        self.__middleware_groups[key] = middleware

        return self

    def alias_middleware(self, key, middleware):
        self.middleware[key] = middleware
        return self

    def get(self, uri, action):
        return self.__add_route(["GET", "HEAD"], uri, action)

    def post(self, uri, action):
        return self.__add_route(["POST"], uri, action)

    def put(self, uri, action):
        return self.__add_route(["PUT"], uri, action)

    def patch(self, uri, action):
        return self.__add_route(["PATCH"], uri, action)

    def delete(self, uri, action):
        return self.__add_route(["DELETE"], uri, action)

    def option(self, uri, action):
        return self.__add_route(["OPTION"], uri, action)

    def name(self, value: str):
        self.__attributes["name"] = value

        return self

    def __add_route(self, methods, uri, action):
        route = self.__create_route(methods, uri, action)

        self.routes.add(route)

        return self

    def __create_route(self, methods, uri, action):
        controller_action = self.__convert_to_controller_action(action)

        return self.__new_route(methods, uri, controller_action)

    def __new_route(self, methods, uri, action):
        route = (
            Route(self.__attributes, methods, uri, action)
            .set_router(self)
            .set_application(self.__app)
        )

        self.__attributes = self.__get_default_attributes()

        return route

    def __convert_to_controller_action(self, action):
        if callable(action) and (action.__name__ == "<lambda>"):
            return {"uses": action}

        if isinstance(action, list):
            controller_class, controller_action = action

            return {
                "controller_class": controller_class,
                "controller_action": controller_action,
                "type": "controller",
            }

        if hasattr(action, "__call__"):
            return {
                "controller_class": action,
                "controller_action": "__call__",
                "type": "controller",
            }

    def dispatch(self, request: Request):
        self.current_request = request

        return self.__dispatch_to_route(request)

    def __dispatch_to_route(self, request: Request):
        return self.__run_route(request, self.__find_matching_route(request))

    def __run_route(self, request: Request, route: Route):
        if not route:
            response = self.__app.make("response")
            response.set_content("Route not found")
            response.set_status("404 NOT_FOUND")
            response.set_headers("Content-Type", "text/plain")

            return response

        content = route.run()

        if isinstance(content, ResponseFactory):
            return response
        elif isinstance(content, str):
            response = self.__app.make("response")
            response.set_content(content)
            response.set_status("200 OK")
            response.set_headers("Content-Type", "text/plain")
            return response
        elif isinstance(content, ViewFactory):
            response = self.__app.make("response")
            response.set_content(content.get_content())
            response.set_status("200 OK")
            response.set_headers("Content-Type", "text/html")
            return response
        elif isinstance(content, Redirector):
            response = self.__app.make("response")
            response.set_content("Redirecting")
            response.set_status("302 FOUND")
            response.set_headers("Location", content.url)
            return response

    def __find_matching_route(self, request: Request):
        matched_route: Route = self.routes.match(request)

        if matched_route:
            return matched_route.set_router(self).set_application(self.__app)
        else:
            return None

    def get_routes(self):
        return self.routes

    def register_path(self, path: str):
        self.__registered_paths.append(path)

    def get_registered_paths(self):
        return self.__registered_paths

    def group(self, attributes: Dict[str, Any], route_resolver: Any):
        self.__set_attributes(attributes)

        route_resolver(self)

    def __set_attributes(self, attributes: Dict[str, Any]):
        valid_attributes = {
            key: value
            for key, value in attributes.items()
            if key in self.__allowed_attributes
        }

        for key, value in valid_attributes.items():
            if key == "middleware":
                self.__set_middleware(value)
            else:
                self.__attributes[key] = value

    def __get_default_attributes(self):
        return {
            "as": None,
            "name": None,
            "prefix": None,
            "middleware": [],
        }

    def __set_middleware(self, middleware: List[Any]):
        self.__attributes["middleware"] += middleware
