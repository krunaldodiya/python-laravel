import json

from Illuminate.Helpers.dd import convert_values_to_string


class Logger:
    def __init__(self, app) -> None:
        self.__app = app

    def log(self, info):
        print("logging", info)

    def dd(self, info):
        try:
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

            response = self.__app.make("response")
            events = self.__app.make("events")

            response.set_status("200 OK")
            response.set_headers("Content-Type", "application/json")
            response.set_content(data)

            events.dispatch("response_sent", {"response": response})
        finally:
            exit()
