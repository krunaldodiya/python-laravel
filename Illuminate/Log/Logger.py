import json

from Illuminate.Helpers.dd import convert_values_to_string


class Logger:
    def __init__(self, app) -> None:
        self.__app = app

    def log(self, info):
        print("logging", info)

    def dd(self, info):
        data = vars(info)
        dict_obj = convert_values_to_string(data)
        string_obj = json.dumps(dict_obj)

        response = self.__app.make("response")
        response.set_data(string_obj)
