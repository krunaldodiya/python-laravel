import re

from typing import List
from Illuminate.Routing.Route import Route
from Illuminate.Contracts.Http.Request import Request


class RouteCollection:
    def __init__(self) -> None:
        self.routes = {}
        self.all_routes = {}

    def add(self, route: Route) -> None:
        for method in route.methods:
            method_wise_routes = self.routes.setdefault(method, {})
            method_wise_routes[route.uri] = route

        self.all_routes[route.uri] = route

    def match(self, request: Request):
        routes = [route for route in self.routes.get(request.method, {}).values()]

        return self.__match_against_routes(request, routes)

    def __match_against_routes(self, request: Request, routes: List[Route]):
        matched_routes = []

        for route in routes:
            matched = self.__run_match(request, route)

            if matched:
                matched_routes.append(matched)

        return matched_routes[-1] if matched_routes else None

    def __run_match(self, request: Request, route: Route):
        request_path = request.path.strip("/")

        route_uri = route.uri.strip("/")

        pattern = re.escape(route_uri)

        params = re.findall(r":(\w+)", pattern)

        if not params:
            return route if route_uri == request_path else None

        for param in params:
            pattern = pattern.replace(f":{param}", r"(?P<" + param + r">[^/]+)")

        pattern = f"^{pattern}$"

        match = re.match(pattern, request_path)

        if match:
            return route.set_route_params(match.groupdict()).set_query_params(request)
        else:
            return None
