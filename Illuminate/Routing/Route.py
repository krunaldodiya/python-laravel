from importlib import import_module


class Route:
    def __init__(self, methods, uri, action) -> None:
        self.__methods = methods
        self.__uri = uri
        self.__action = action

        self.__router = None
        self.__app = None

    @property
    def methods(self):
        return self.__methods

    @property
    def uri(self):
        return self.__uri

    @property
    def action(self):
        return self.__action

    def set_router(self, router):
        self.__router = router
        return self

    def set_application(self, app):
        self.__app = app
        return self

    def run(self):
        action = None

        if self.action.get("controller_action"):
            action = self.__run_controller()
        else:
            action = self.__run_callable()

        dependencies = self.__app.get_dependencies(action)

        return action(**dependencies)

    def __run_callable(self):
        return self.action["uses"]

    def __run_controller(self):
        controller_module = import_module(
            self.action["controller_module"], package=None
        )

        controller_class = getattr(controller_module, self.action["controller_name"])

        controller_object = self.__app.make(controller_class)

        return getattr(controller_object, self.action["controller_action"])
