import json


class Request:
    def __init__(self) -> None:
        pass

    def initialize(self, environ) -> None:
        self.http_host = environ["HTTP_HOST"]
        self.server_name = environ["SERVER_NAME"]
        self.server_port = environ["SERVER_PORT"]
        self.query_string = environ["QUERY_STRING"]
        self.path_info = environ["PATH_INFO"]
        self.request_method = environ["REQUEST_METHOD"]

        self.params = {}

    def set_params(self, params):
        self.params = params

    def get(self, param):
        return self.params.get(param)

    def __str__(self) -> str:
        return json.dumps(self.__dict__)
