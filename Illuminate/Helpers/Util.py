import copy


class Util:
    @staticmethod
    def convert_values_to_string(data):
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

    @staticmethod
    def to_dict(cookie):
        cookie_dict = {}

        for pair in cookie.split(";"):
            key, value = pair.strip().split("=")

            cookie_dict[key.strip()] = value.strip()

        return cookie_dict
