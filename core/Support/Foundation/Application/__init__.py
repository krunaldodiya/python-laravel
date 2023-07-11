import re
from waitress import serve
from core.Support.Facades.Request import Request
from core.Support.Facades.Route import Route
from core.Support.Facades.View import View
from core.Support.Foundation.Container import Container
from core.http_request import HttpRequest
from core.template import Template
from core.controller import Controller

from core.router import Router


class Application:
    def __init__(self) -> None:
        self.__container: Container = Container()

        self.register_providers()
        self.register_facades()

        self.__request = self.resolve("request")

        self.__router = self.resolve("route")

    def make(self, key: str, make_args=None):
        return self.__container.resolve(key, make_args)

    def resolve(self, key: str):
        return self.__container.resolve(key, None)

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
        self.singleton("request", lambda _: HttpRequest())
        self.singleton("route", lambda _: Router())
        self.singleton("view", lambda _: Template())

    def register_facades(self):
        Request.app = self
        Route.app = self
        View.app = self

        Controller.app = self

    def match_router_pattern(self, router_pattern, request):
        pattern = re.escape(router_pattern)

        params = re.findall(r":(\w+)", pattern)

        if not params:
            return router_pattern == request.path_info

        for param in params:
            pattern = pattern.replace(f":{param}", r"(?P<" + param + r">[^/]+)")

        pattern = f"^{pattern}$"

        match = re.match(pattern, request.path_info)

        if match:
            router_params = {param: str(match.group(param)) for param in params}

            request.set_params(router_params)

            return {key: value for key, value in match.groupdict().items()}

        return None

    def load_route(self):
        matched_routes = [
            route
            for route in self.__router.routes
            if route["request_method"] == self.__request.request_method
            and self.match_router_pattern(route["path"], self.__request)
        ]

        if matched_routes:
            matched_route = matched_routes[-1]

            controller_name = matched_route["controller"]
            callable_method = matched_route["callable_method"]

            if controller_name:
                controller = self.resolve(controller_name)
                method = getattr(controller, callable_method)
            else:
                method = callable_method

            method(self.__request)

            response_body = method(self.__request)

            return response_body, "200 OK"
        else:
            response_body = "Route not found."

            return response_body, "404 NOT_FOUND"

    def request_handler(self, environ, start_response):
        self.__request.initialize(environ)

        response_body, status = self.load_route()

        response_headers = [
            ("Content-type", "text/html"),
        ]

        start_response(status, response_headers)

        return [response_body.encode("utf-8")]

    def run(self, host="localhost", port=5000):
        serve(self.request_handler, host=host, port=port)
