class Router:
    def __init__(self, app) -> None:
        self.__app = app

        self.routes = []

        self.middleware = {}
        self.middleware_groups = {}
        self.middleware_priorities = {}

    def middleware_group(self, key, middleware):
        self.middleware_groups[key] = middleware
        return self

    def alias_middleware(self, key, middleware):
        self.middleware[key] = middleware
        return self

    def get(self, route, handler):
        self.make(route, handler, "GET")

    def post(self, route, handler):
        self.make(route, handler, "POST")
