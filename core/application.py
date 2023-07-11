import re
from waitress import serve
from core.request import Request
from core.router import Router

router = Router()
request = Request()


class Application:
    def __init__(self) -> None:
        self.request = request
        self.router = router
        self.__bindings = {}

    @property
    def bindings(self):
        return self.__bindings

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
            for route in self.router.routes
            if route["request_method"] == request.request_method
            and self.match_router_pattern(route["path"], self.request)
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

            method(self.request)

            response_body = method(self.request)

            return response_body, "200 OK"
        else:
            response_body = "Route not found."

            return response_body, "404 NOT_FOUND"

    def request_handler(self, environ, start_response):
        self.request.initialize(environ)

        response_body, status = self.load_route()

        response_headers = [
            ("Content-type", "text/html"),
        ]

        start_response(status, response_headers)

        return [response_body.encode("utf-8")]

    def bind(self, key, binding):
        self.__bindings[key] = lambda: binding()

    def resolve(self, key):
        function = self.__bindings[key]
        return function()

    def run(self, host="localhost", port=5000):
        serve(self.request_handler, host=host, port=port)

    def test(self):
        return self.bindings["router"]
