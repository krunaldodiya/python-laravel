from urllib.parse import parse_qs


class HttpRequest:
    def __init__(self) -> None:
        self.http_host = None
        self.server_name = None
        self.server_port = None
        self.query_string = None
        self.path_info = None
        self.request_method = None
        self.body = None

    def initialize(self, environ) -> None:
        self.http_host = environ["HTTP_HOST"]
        self.server_name = environ["SERVER_NAME"]
        self.server_port = environ["SERVER_PORT"]
        self.query_string = environ["QUERY_STRING"]
        self.path_info = environ["PATH_INFO"]
        self.request_method = environ["REQUEST_METHOD"]

        self.body = (
            parse_qs(environ["wsgi.input"].read().decode())
            if self.request_method == "POST"
            else None
        )

        self.params = {}

    def set_params(self, params):
        self.params = params

    def get(self, param):
        return self.params.get(param)
