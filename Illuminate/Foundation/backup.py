from importlib import import_module
import inspect
import re
from Illuminate.Support.Facades.Response import Response
from Illuminate.Http.ResponseFactory import ResponseFactory


class Backup:
    def match_router_pattern(self, request, route_path):
        pattern = re.escape(route_path)

        params = re.findall(r":(\w+)", pattern)

        if not params:
            return route_path == request.path_info

        for param in params:
            pattern = pattern.replace(f":{param}", r"(?P<" + param + r">[^/]+)")

        pattern = f"^{pattern}$"

        match = re.match(pattern, request.path_info)

        if match:
            router_params = {param: str(match.group(param)) for param in params}

            request.set_params(router_params)

            return {key: value for key, value in match.groupdict().items()}

        return None

    def get_dependencies(self, class_info):
        def get_instance(info):
            module = import_module(info.__module__, package=None)
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
            module = import_module(matched_route["module_path"], package=None)

            module_class = getattr(module, matched_route["module_name"])

            dependencies = self.get_dependencies(module_class)

            self.singleton(
                matched_route["module_path"], lambda: module_class(*dependencies)
            )

            return self.resolve(matched_route["module_path"])

    def make_response(self):
        request = self.resolve("request")
        router = self.resolve("router")

        matched_routes = [
            route
            for route in router.routes
            if route["request_method"] == request.request_method
            and self.match_router_pattern(request, route["path"])
        ]

        if matched_routes:
            matched_route = matched_routes[-1]

            if matched_route["callable"]:
                method = matched_route["action"]
            else:
                controller = self.get_controller(matched_route)
                method = getattr(controller, matched_route["action_name"])

            response = method(request)

            if isinstance(response, ResponseFactory):
                return response
            else:
                return Response.make(response, "200 OK")
        else:
            return Response.make("Route not found.", "404 NOT_FOUND")
