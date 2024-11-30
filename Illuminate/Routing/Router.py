from typing import Any, Dict, List
from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Events import Dispatcher
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Helpers.Util import Util
from Illuminate.Routing.Events.PreparingResponse import PreparingResponse
from Illuminate.Routing.Events.ResponsePrepared import ResponsePrepared
from Illuminate.Routing.Events.Routing import Routing
from Illuminate.Http.Request import Request
from Illuminate.Pipeline.Pipeline import Pipeline
from Illuminate.Routing.MiddlewareNameResolver import MiddlewareNameResolver
from Illuminate.Routing.Route import Route
from Illuminate.Routing.RouteCollection import RouteCollection
from Illuminate.Routing.RouteGroup import RouteGroup
from Illuminate.Support.helpers import tap


class Router:
    def __init__(self, app: Application, events: Dispatcher) -> None:
        self.__app = app

        self.__events = events

        self._route_collection = RouteCollection()

        self.current_route = None

        self.current_request = None

        self.__middleware = {}

        self.__middleware_groups = {}

        self.__middleware_priorities = []

        self.__registered_paths = []

        self._group_stack = []

    @property
    def app(self):
        return self.__app

    @property
    def group_stack(self):
        return self._group_stack

    @group_stack.setter
    def group_stack(self, group_stack):
        self._group_stack = group_stack

    @property
    def events(self):
        return self.__events

    @property
    def route_collection(self):
        return self._route_collection

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
        return self.add_route(["GET", "HEAD"], uri, action)

    def post(self, uri, action):
        return self.add_route(["POST"], uri, action)

    def put(self, uri, action):
        return self.add_route(["PUT"], uri, action)

    def patch(self, uri, action):
        return self.add_route(["PATCH"], uri, action)

    def delete(self, uri, action):
        return self.add_route(["DELETE"], uri, action)

    def option(self, uri, action):
        return self.add_route(["OPTION"], uri, action)

    def add_route(self, methods, uri, action):
        route = self._create_route(methods, uri, action)

        self._route_collection.add(route)

        return self

    def _create_route(self, methods, uri, action):
        action = self._convert_to_controller_action(action)

        route = self.new_route(
            methods,
            self._prefix(uri),
            action,
        )

        if self.has_group_stack():
            self._merge_group_attributes_into_routes(route)

        return route

    def _merge_group_attributes_into_routes(self, route: Route):
        route.set_action(
            self.merge_with_last_group(route.get_action(), False),
        )

    def _convert_to_controller_action(self, action):
        if Util.is_function(action):
            return {"uses": action}

        if isinstance(action, list) and len(action) == 2:
            controller_class, controller_action = action

            return {
                "controller": controller_class,
                "uses": controller_action,
            }

        if hasattr(action, "__call__"):
            return {
                "controller": action,
                "uses": "__call__",
            }

        raise Exception("BadMethodCallException")

    def _prefix(self, uri: str):
        last_prefix = self.get_last_group_prefix()

        trimmed_last_prefix = last_prefix.strip("/")

        trimmed_uri = uri.strip("/")

        return f"{trimmed_last_prefix}/{trimmed_uri}"

    def get_last_group_prefix(self):
        if self.has_group_stack():
            last_group_stack = self.group_stack[-1]

            return last_group_stack.get("prefix", "")

        return ""

    def has_group_stack(self):
        return bool(self.group_stack)

    def new_route(self, methods, uri, action):
        return Route(methods, uri, action).set_router(self).set_application(self.app)

    def dispatch(self, request: Request):
        self.current_request = request

        data = self.dispatch_to_route(request)

        return data

    def dispatch_to_route(self, request: Request):
        return self._run_route(request, self._find_route(request))

    def _run_route(self, request: Request, route: Route):
        request.set_route_resolver(lambda: route)

        return self.prepare_response(
            request,
            self._run_route_within_stack(route, request),
        )

    def _run_route_within_stack(self, route: Route, request: Request):
        middleware = self.gather_route_middleware(route)

        output = (
            Pipeline(self.__app)
            .send(request)
            .through(middleware)
            .then(lambda request: self.prepare_response(request, route.run()))
        )

        return output

    @classmethod
    def to_response(cls, request: Request, response: Any):
        return response

    def prepare_response(self, request: Request, response: Any):
        if not isinstance(request, Request):
            response = request

        self.events.dispatch(PreparingResponse(request, response))

        return tap(
            self.to_response(request, response),
            lambda response: self.events.dispatch(ResponsePrepared(request, response)),
        )

    def gather_route_middleware(self, route):
        route_middleware = route.gather_middleware()

        resolved_middleware = self.__resolve_middlware(route_middleware)

        sorted_middleware = self.__sort_middleware_by_priorities(resolved_middleware)

        return sorted_middleware

    def __resolve_middlware(self, middleware: List[Any]):
        return (
            collect(middleware)
            .map(
                lambda name: MiddlewareNameResolver.resolve(
                    name, self.__middleware, self.__middleware_groups
                )
            )
            .filter(lambda name: name is not None)
            .flatten()
            .all()
        )

    def __sort_middleware_by_priorities(self, middleware: Dict[Any, Any]):
        priorities = []

        non_priorities = []

        for key, item in middleware:
            if item in self.__middleware_priorities:
                priorities.append(item)
            else:
                non_priorities.append(item)

        return priorities + non_priorities

    def _find_route(self, request: Request):
        self.events.dispatch(Routing(request))

        route = self._route_collection.match(request)

        self.current_route = route

        route.set_application(self.__app)

        self.__app.instance(Route, route)

        return route

    def get_routes(self):
        return self._route_collection

    def register_path(self, path: str):
        self.__registered_paths.append(path)

    def get_registered_paths(self):
        return self.__registered_paths

    def group(self, attributes: Dict[str, Any], route_resolver: Any):
        group_routes = (
            route_resolver if isinstance(route_resolver, list) else [route_resolver]
        )

        for group_route in group_routes:
            self._update_group_stack(attributes)

            self._load_routes(group_route)

            self.group_stack.pop()

    def _update_group_stack(self, attributes):
        if self.has_group_stack():
            attributes = self.merge_with_last_group(attributes)

        self.group_stack.append(attributes)

    def merge_with_last_group(self, new_attributes, prepend_existing_prefix=True):
        last_group_stack = self.group_stack[-1]

        return RouteGroup.merge(
            new_attributes, last_group_stack, prepend_existing_prefix
        )

    def _load_routes(self, route_resolver):
        try:
            route_resolver(self)
        except Exception as e:
            raise e

    def __getattr__(cls, attribute, *args, **kwargs):
        if not cls.route_collection.all_routes:
            return

        last_route = list(cls.route_collection.all_routes.values())[-1]

        allowed_dynamic_methods = ["name", "middleware"]

        if attribute in allowed_dynamic_methods:
            return getattr(last_route, attribute)

        raise Exception("BadMethodCallException")
