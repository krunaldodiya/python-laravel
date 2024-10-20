class WSGIServer:
    __server = None

    def __init__(self, environ, start_response) -> None:
        self.environ = environ
        self.start_response = start_response

        self.scheme = environ["wsgi.url_scheme"]
        self.server_name = environ["SERVER_NAME"]
        self.server_port = environ["SERVER_PORT"]

        self.host = self.get_host()

        self.query_string = environ["QUERY_STRING"]
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.raw_path = environ["RAW_URI"]

        self.headers = {}
        self.cookies = {}

    @classmethod
    def create_server(cls, environ, start_response):
        server = WSGIServer(environ, start_response)
        WSGIServer.__server = server
        return server

    @classmethod
    def get_server(cls):
        return WSGIServer.__server

    def send(self):
        try:
            return ["test".encode("utf-8")]
        finally:
            print("done")

    def get_host(self):
        return (
            f"{self.scheme}://{self.server_name}"
            if self.server_port in [80, 443]
            else f"{self.scheme}://{self.server_name}:{self.server_port}"
        )
