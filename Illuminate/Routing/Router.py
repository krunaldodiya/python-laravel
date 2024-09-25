from Illuminate.Contracts.Events import Dispatcher
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Http.Request import Request
from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Routing.LambdaController import LambdaController
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

        self.middleware = {}
        self.middleware_groups = {}
        self.middleware_priorities = {}

        self.__registered_paths = []

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
        route = self.__create_route(methods, uri, action)

        self.routes.add(route)

    def __create_route(self, methods, uri, action):
        action = self.__convert_to_controller_action(action)

        return self.__new_route(methods, uri, action)

    def __new_route(self, methods, uri, action):
        return Route(methods, uri, action).set_router(self).set_application(self.__app)

    def __convert_to_controller_action(self, action):
        """
        Convert the given action into a controller action.
        """

        # If action is a list, assume it's a controller and method pair.
        if isinstance(action, list):
            controller, controller_action = action

            return {
                "controller_action": controller_action,
                "controller_module": f"{controller.__module__}",
                "controller_name": f"{controller.__name__}",
            }

        # If the action is a lambda function (anonymous function), wrap it in a LambdaController
        if callable(action) and (action.__name__ == "<lambda>"):
            lambda_controller = LambdaController(action)
            return {
                "uses": lambda_controller,
                "type": "lambda_controller",
                "module": lambda_controller.__class__.__module__,
            }

        # If action is a class with a __call__ method, treat it as an invokable controller.
        if hasattr(action, "__call__") and not isinstance(action, LambdaController):
            return {
                "uses": action.__class__.__name__,
                "controller_module": action.__class__.__module__,
                "type": "invokable",
            }

        # Default fallback if it's a simple callable function
        return {"uses": action}

    def dispatch(self, request: Request):
        self.current_request = request

        return self.__dispatch_to_route(request)

    def __dispatch_to_route(self, request: Request):
        try:
            self.current = self.__find_matching_route(request)

            return self.__run_route(request, self.current)
        except RouteNotFound:
            response = self.__app.make("response")
            response.set_content("Route not found")
            response.set_status("404 NOT_FOUND")
            response.set_headers("Content-Type", "text/plain")

            return response

    def __run_route(self, request: Request, route: Route):
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
            raise RouteNotFound("Route not found")

    def get_routes(self):
        return self.routes

    def register_path(self, path: str):
        self.__registered_paths.append(path)

    def get_registered_paths(self):
        return self.__registered_paths
