from Illuminate.Routing.Route import Route


class RouteCollection:
    def __init__(self) -> None:
        self.routes = {}
        self.all_routes = []

    def add(self, route: Route) -> None:
        for method in route.methods:
            self.routes[method] = route

        self.all_routes.append(route)
