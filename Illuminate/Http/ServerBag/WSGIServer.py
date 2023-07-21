class WSGIServer:
    __server = None

    def __init__(self, environ, start_response) -> None:
        self.environ = environ
        self.start_response = start_response

        self.scheme = environ["wsgi.url_scheme"]
        self.server_name = environ["SERVER_NAME"]
        self.server_port = environ["SERVER_PORT"]

        self.server_url = self.get_server_url()

        self.query_string = environ["QUERY_STRING"]
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.raw_path = environ["RAW_URI"]

        self.headers = {}
        self.cookies = {}

    @staticmethod
    def create_server(environ, start_response):
        server = WSGIServer(environ, start_response)
        WSGIServer.__server = server
        return server

    @staticmethod
    def get_server():
        return WSGIServer.__server

    def send(self):
        try:
            return ["test".encode("utf-8")]
        finally:
            print("done")

    def get_server_url(self):
        return (
            f"{self.scheme}://{self.server_name}"
            if self.server_port in [80, 443]
            else f"{self.scheme}://{self.server_name}:{self.server_port}"
        )
