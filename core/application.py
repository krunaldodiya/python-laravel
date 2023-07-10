import re
from wsgiref.simple_server import make_server
from Controllers.home import HomeController
from core.request import Request
from core.router import Router

router = Router()
request = Request()


class Application:
    def __init__(self) -> None:
        self.request = request
        self.router = router

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
            if self.match_router_pattern(route["path"], self.request)
        ]

        if matched_routes:
            matched_route = matched_routes[-1]

            response_body = matched_route["handler"](HomeController(), self.request)

            return response_body, "200 OK"
        else:
            response_body = "Route not found."

            return response_body, "404 NOT_FOUND"

    def route_handler(self, environ, start_response):
        self.request.initialize(environ)

        response_body, status = self.load_route()

        response_headers = [
            ("Content-type", "text/plain"),
        ]

        start_response(status, response_headers)

        return [response_body.encode("utf-8")]

    def boot(self, host="localhost", port=5000):
        self.server = make_server(host, port, app=self.route_handler)

    def run(self):
        self.server.serve_forever()
