import inspect
import json

from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Helpers.Util import Util


class Logger:
    def __init__(self, app: Application) -> None:
        self.__app = app

    def log(self, info):
        print("logging", info)

    def dd(self, info):
        if isinstance(info, str):
            data = info
        elif isinstance(info, (int, float, bool)):
            data = str(info)
        elif isinstance(info, (list, dict)):
            data = json.dumps(Util.convert_values_to_string(info))
        elif callable(info):
            data = json.dumps(Util.convert_values_to_string(vars(info)))
        else:
            data = (
                json.dumps(Util.convert_values_to_string(vars(info)))
                if hasattr(info, "__dict__")
                else str(info)
            )

        return json.loads(data)

    @classmethod
    def caller_info(cls):
        stack = inspect.stack()

        caller_frame = stack[2]

        function_name = caller_frame.function

        module_name = caller_frame.frame.f_globals["__name__"]

        instance = caller_frame.frame.f_locals.get("self", None)

        if instance:
            class_name = instance.__class__.__name__
        else:
            class_name = None

        print(f"Called from: {module_name}.{class_name}.{function_name}")
