from core.Support.Facades.Facade import Facade


class RouterFacade(metaclass=Facade):
    def get(self, route, handler):
        pass

    def post(self, route, handler):
        pass


class Router:
    def __init__(self) -> None:
        self.routes = []

    def get(self, route, handler):
        self.make(route, handler, "GET")

    def post(self, route, handler):
        self.make(route, handler, "POST")

    def make(self, route, handler, requested_method):
        if not (callable(handler) or (isinstance(handler, list) and len(handler) == 2)):
            raise Exception("Invalid route")

        if type(handler) == list:
            controller, method = handler
        else:
            controller, method = None, handler

        self.routes.append(
            {
                "path": route,
                "request_method": requested_method,
                "controller": controller,
                "callable_method": method,
            }
        )
