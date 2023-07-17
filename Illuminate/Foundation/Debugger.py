import copy


class Debugger:
    def __init__(self, app) -> None:
        self.__app = app

    def dd(self, data):
        return self.__convert_values_to_string(data)

    def __convert_values_to_string(self, data):
        copied_data = copy.copy(data)

        def converter(obj):
            if isinstance(obj, dict):
                return {key: converter(value) for key, value in obj.items()}

            elif isinstance(obj, list):
                return [converter(value) for value in obj]

            elif callable(obj):
                return obj.__module__ + "." + obj.__name__

            return str(obj)

        return converter(copied_data)
