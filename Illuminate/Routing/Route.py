from typing import Any, Dict


class Route:
    def __init__(self, attributes: Dict[str, Any], methods, uri, action) -> None:
        self.__name: str = attributes.get("name", "")

        self.__alias: str = attributes.get("as", "")

        self.__prefix: str = attributes.get("prefix", "")

        self.__middleware = attributes.get("middleware", [])

        self.__computed_middleware = None

        self.__uri = f"{self.prefix.strip('/')}/{uri}" if self.prefix else uri

        self.__action = action

        self.__methods = methods

        self.__params = {}

        self.__app = None

        self.__router = None

    @property
    def name(self):
        return self.__name

    @property
    def alias(self):
        return self.__alias

    @property
    def prefix(self):
        return self.__prefix

    @property
    def middleware(self):
        return self.__middleware

    @property
    def computed_middleware(self):
        return self.__computed_middleware

    @property
    def uri(self):
        return self.__uri

    @property
    def action(self):
        return self.__action

    @property
    def methods(self):
        return self.__methods

    @property
    def params(self):
        return self.__params

    @property
    def app(self):
        return self.__app

    @property
    def router(self):
        return self.__router

    def set_router(self, router):
        self.__router = router

        return self

    def set_application(self, app):
        self.__app = app

        return self

    def run(self):
        action = None

        type = self.action.get("type")

        if type in ["controller", "callable"]:
            action = self.__run_controller()
        else:
            action = self.__run_callable()

        if not action:
            raise Exception("Invalid route action")

        dependencies = self.app.get_dependencies(action)

        return action(**dependencies)

    def __get_controller(self):
        return self.app.make(self.action["controller_class"])

    def __run_controller(self):
        controller_object = self.__get_controller()

        return getattr(controller_object, self.action["controller_action"])

    def __run_callable(self):
        return self.action["uses"]

    def gather_middleware(self):
        if not self.__computed_middleware:
            self.__computed_middleware = (
                self.__middleware + self.__controller_middleware()
            )

        return self.__computed_middleware

    def __controller_middleware(self):
        type = self.action.get("type")

        if type not in ["controller", "callable"]:
            return []

        controller_object = self.__get_controller()

        return getattr(controller_object, "middleware", [])

    def set_params(self, params: Dict[str, Any]):
        self.__params = params

        return self
