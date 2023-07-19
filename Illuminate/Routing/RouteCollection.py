import re
from typing import List
from Illuminate.Http.Request import Request
from Illuminate.Routing.Route import Route


class RouteCollection:
    def __init__(self) -> None:
        self.routes = {}
        self.all_routes = {}

    def add(self, route: Route) -> None:
        for method in route.methods:
            method_wise_routes = self.routes.setdefault(method, {})
            method_wise_routes[route.uri] = route

        self.all_routes[route.uri] = route

    def match(self, request: Request) -> None:
        routes = [
            route for route in self.routes.get(request.server.method, {}).values()
        ]

        return self.__match_against_routes(request, routes)

    def __match_against_routes(self, request: Request, routes: List[Route]):
        matched = None

        for route in routes:
            route = self.__run_match(request, route)

            if route:
                matched = route

        return matched

    def __run_match(self, request: Request, route: Route):
        pattern = re.escape(route.uri)

        params = re.findall(r":(\w+)", pattern)

        if not params:
            return route if route.uri == request.server.path else None

        for param in params:
            pattern = pattern.replace(f":{param}", r"(?P<" + param + r">[^/]+)")

        pattern = f"^{pattern}$"

        match = re.match(pattern, request.server.path)

        return route if match else None
