from importlib import import_module
import inspect
import re

from waitress import serve

from Illuminate.Support.Facades.Response import Response
from Illuminate.Support.Foundation.Container import Container
from Illuminate.file_loader import load_files
from Illuminate.http_request import HttpRequest
from Illuminate.http_response import HttpResponse
from Illuminate.template import Template

from Illuminate.router import Router


class Application:
    def __init__(self) -> None:
        self.__container: Container = Container()

        self.register_providers()

        self.__request = self.resolve("request")
        self.__router = self.resolve("route")

    def make(self, key: str):
        return self.__container.resolve(key)

    def resolve(self, key: str):
        return self.__container.resolve(key)

    def bind(self, key: str, binding_resolver):
        self.__container.set_binding(
            key,
            binding_resolver,
            False,
        )

    def singleton(self, key: str, binding_resolver):
        self.__container.set_singleton(
            key,
            binding_resolver,
            True,
        )

    def register_providers(self):
        self.singleton("request", lambda: HttpRequest())
        self.singleton("response", lambda: HttpResponse())
        self.singleton("route", lambda: Router())
        self.singleton("view", lambda: Template())

    def match_router_pattern(self, route_path):
        pattern = re.escape(route_path)

        params = re.findall(r":(\w+)", pattern)

        if not params:
            return route_path == self.__request.path_info

        for param in params:
            pattern = pattern.replace(f":{param}", r"(?P<" + param + r">[^/]+)")

        pattern = f"^{pattern}$"

        match = re.match(pattern, self.__request.path_info)

        if match:
            router_params = {param: str(match.group(param)) for param in params}

            self.__request.set_params(router_params)

            return {key: value for key, value in match.groupdict().items()}

        return None

    def get_dependencies(self, class_info):
        def get_instance(info):
            module = import_module(info.__module__)
            module_class = getattr(module, info.__name__)

            return create_instance(module_class)

        def create_instance(class_info):
            dependencies = self.get_dependencies(class_info)
            return class_info(*dependencies)

        args_info = inspect.getfullargspec(class_info)

        return [
            get_instance(args_info.annotations[arg])
            for arg in args_info.args
            if arg != "self"
        ]

    def get_controller(self, matched_route):
        try:
            return self.resolve(matched_route["module_path"])
        except:
            module = import_module(matched_route["module_path"])

            module_class = getattr(module, matched_route["module_name"])

            dependencies = self.get_dependencies(module_class)

            self.singleton(
                matched_route["module_path"], lambda: module_class(*dependencies)
            )

            return self.resolve(matched_route["module_path"])

    def make_response(self):
        matched_routes = [
            route
            for route in self.__router.routes
            if route["request_method"] == self.__request.request_method
            and self.match_router_pattern(route["path"])
        ]

        if matched_routes:
            matched_route = matched_routes[-1]

            if matched_route["callable"]:
                method = matched_route["action"]
            else:
                controller = self.get_controller(matched_route)
                method = getattr(controller, matched_route["action_name"])

            response = method(self.__request)

            if isinstance(response, HttpResponse):
                return response
            else:
                return Response.make(response, "200 OK")
        else:
            return Response.make("Route not found.", "404 NOT_FOUND")

    def __call__(self, environ, start_response):
        load_files("routes")

        self.__request.initialize(environ)

        http_response: HttpResponse = self.make_response()

        start_response(http_response.status, http_response.response_headers)

        return [http_response.response_body]

    def run(self, host="localhost", port=5000):
        serve(self, host=host, port=port)
