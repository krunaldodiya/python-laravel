import types

from typing import Any, Dict, List
from Illuminate.Contracts.Events import Dispatcher
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Contracts.Http.Response import Response
from Illuminate.Database.Collection import Collection
from Illuminate.Http.Request import Request
from Illuminate.Pipeline.Pipeline import Pipeline
from Illuminate.Routing.MiddlewareNameResolver import MiddlewareNameResolver
from Illuminate.Routing.Route import Route
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Routing.RouteCollection import RouteCollection


class RouteNotFound(Exception):
    pass


class Router:
    def __init__(self, app: Application, events: Dispatcher) -> None:
        self.__app = app

        self.__events = events

        self.__route_collection = RouteCollection()

        self.current_route = None

        self.current_request = None

        self.__middleware = {}

        self.__middleware_groups = {}

        self.__middleware_priorities = []

        self.__registered_paths = []

        self.__attributes = self.__get_default_attributes()

        self.__allowed_attributes = self.__attributes.keys()

    @property
    def app(self):
        return self.__app

    @property
    def events(self):
        return self.__events

    @property
    def route_collection(self):
        return self.__route_collection

    @property
    def attributes(self):
        return self.__attributes

    def get_middleware(self):
        return self.__middleware

    def get_middleware_groups(self):
        return self.__middleware_groups

    def get_middleware_priorities(self):
        return self.__middleware_priorities

    def middleware_priorities(self, middleware_priorities: List[Any]):
        self.__middleware_priorities = middleware_priorities

        return self

    def middleware(self, middleware: List[Any]):
        self.__set_middleware(middleware)

        return self

    def middleware_group(self, key, middleware):
        self.__middleware_groups[key] = middleware

        return self

    def alias_middleware(self, key, middleware):
        self.__middleware[key] = middleware
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

        self.__route_collection.add(route)

        return self

    def __create_route(self, methods, uri, action):
        controller_action = self.__convert_to_controller_action(action)

        return self.__new_route(methods, uri, controller_action)

    def __new_route(self, methods, uri, action):
        return Route(self, methods, uri, action)

    def __convert_to_controller_action(self, action):
        if isinstance(action, types.FunctionType) or (
            isinstance(action, types.LambdaType) and action.__name__ == "<lambda>"
        ):
            return {"uses": action}

        if isinstance(action, list) and len(action) == 2:
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
                "type": "callable",
            }

        raise Exception("BadMethodCallException")

    def dispatch(self, request: Request):
        self.current_request = request

        data = self.__dispatch_to_route(request)

        return data

    def __dispatch_to_route(self, request: Request):
        matched_route = self.__find_matching_route(request)

        return self.__run_route(request, matched_route)

    def __run_route(self, request: Request, route: Route):
        return self.__run_route_within_stack(request, route)

    def __run_route_within_stack(self, request, route):
        middleware = self.__gather_route_middleware(route)

        return (
            Pipeline(self.__app)
            .send(request)
            .through(middleware)
            .then(lambda response: self.__prepare_response(response, route))
        )

    def __prepare_response(self, output: Request | Response, route: Route):
        response = self.__app.make("response")

        return response.prepare(output, route)

    def __gather_route_middleware(self, route):
        route_middleware = route.gather_middleware()

        resolved_middleware = self.__resolve_middlware(route_middleware)

        sorted_middleware = self.__sort_middleware_by_priorities(resolved_middleware)

        return sorted_middleware

    def __resolve_middlware(self, middleware: List[Any]):
        flattened = (
            Collection(middleware)
            .map(
                lambda name: MiddlewareNameResolver.resolve(
                    name, self.__middleware, self.__middleware_groups
                )
            )
            .filter(lambda name: name is not None)
            .flatten()
            .to_list()
        )

        return flattened

    def __sort_middleware_by_priorities(self, middleware: List[Any]):
        priorities = []

        non_priorities = []

        for item in middleware:
            if item in self.__middleware_priorities:
                priorities.append(item)
            else:
                non_priorities.append(item)

        return priorities + non_priorities

    def __find_matching_route(self, request: Request):
        matched_route: Route = self.__route_collection.match(request)

        if not matched_route:
            raise RouteNotFoundException("Route does not exists")
        else:
            self.current_route = matched_route

            return matched_route

    def get_routes(self):
        return self.__route_collection

    def register_path(self, path: str):
        self.__registered_paths.append(path)

    def get_registered_paths(self):
        return self.__registered_paths

    def group(self, attributes: Dict[str, Any] = {}, route_resolver: Any = None):
        self.__attributes = self.__get_default_attributes()

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
