import json

from Illuminate.Helpers.dd import convert_values_to_string


class Debugger:
    def __init__(self, app) -> None:
        self.__app = app

    def dd(self, data):
        data = vars(data)
        data = convert_values_to_string(data)
        data = json.dumps(data)

        response = self.__app.make("response")

        response.set_data(data)
