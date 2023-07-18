from Illuminate.Routing.Route import Route


class RouteCollection:
    def add(self, route: Route) -> None:
        self.route = route
