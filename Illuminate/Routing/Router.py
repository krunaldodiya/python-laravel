from typing import TYPE_CHECKING, Type
from Illuminate.Http.Request import Request
from Illuminate.Http.ResponseFactory import ResponseFactory
from Illuminate.Routing.Route import Route

from Illuminate.Routing.RouteCollection import RouteCollection
from Illuminate.View.ViewFactory import ViewFactory


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
        self.routes.add(self.__create_route(methods, uri, action))

    def __create_route(self, methods, uri, action):
        action = self.__convert_to_controller_action(action)

        return self.__new_route(methods, uri, action)

    def __new_route(self, methods, uri, action):
        return Route(methods, uri, action).set_router(self).set_application(self.__app)

    def __convert_to_controller_action(self, action):
        if isinstance(action, list):
            controller, controller_action = action

            return {
                "controller_action": controller_action,
                "controller_module": f"{controller.__module__}",
                "controller_name": f"{controller.__name__}",
            }

        if hasattr(action, "__name__") and action.__name__ == "<lambda>":
            raise Exception("lambda function are not allowed")

        return {"uses": action}

    def dispatch(self, request: Request):
        self.current_request = request

        return self.__dispatch_to_route(request)

    def __dispatch_to_route(self, request: Request):
        try:
            self.current = self.__find_matching_route(request)

            return self.__run_route(request, self.current)
        except Exception as e:
            response = self.__app.make("response")
            response.set_content("route not found")

            return response

    def __run_route(self, request: Request, route: Route):
        content = route.run()

        if isinstance(content, ResponseFactory):
            return response

        response = self.__app.make("response")

        if isinstance(content, str):
            response.set_content(content)
            response.set_status("200 OK")
            response.set_headers("Content-Type", "text/plain")

        if isinstance(content, ViewFactory):
            response.set_content(content.get_content())
            response.set_status("200 OK")
            response.set_headers("Content-Type", "text/html")

        return response

    def __find_matching_route(self, request: Request):
        matched: Route = self.routes.match(request)

        if matched:
            return matched.set_router(self).set_application(self.__app)
        else:
            raise Exception(f"<{request.path}> Route not found.")

    def get_routes(self):
        return self.routes

    def register_path(self, path: str):
        self.__registered_paths.append(path)

    def get_registered_paths(self):
        return self.__registered_paths
