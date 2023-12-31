import copy


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
