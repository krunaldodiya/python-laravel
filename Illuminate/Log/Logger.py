import json

from Illuminate.Helpers.dd import convert_values_to_string


class Logger:
    def __init__(self, app) -> None:
        self.__app = app

    def log(self, info):
        print("logging", info)

    def dd(self, info):
        if isinstance(info, str):
            data = info
        elif isinstance(info, (int, float, bool)):
            data = str(info)
        elif isinstance(info, (list, dict)):
            data = json.dumps(convert_values_to_string(info))
        elif callable(info):
            data = json.dumps(convert_values_to_string(vars(info)))
        else:
            data = (
                json.dumps(convert_values_to_string(vars(info)))
                if hasattr(info, "__dict__")
                else str(info)
            )

        return data
