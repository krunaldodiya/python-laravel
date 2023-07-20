class WSGIServer:
    __server = None

    def __init__(self, environ, start_response) -> None:
        self.environ = environ
        self.start_response = start_response

        self.scheme = environ["wsgi.url_scheme"]
        self.server_name = environ["SERVER_NAME"]
        self.server_port = environ["SERVER_PORT"]

        self.server_url = (
            f"{self.scheme}://{self.server_name}"
            if self.server_port in [80, 443]
            else f"{self.scheme}://{self.server_name}:{self.server_port}"
        )

        self.query_string = environ["QUERY_STRING"]
        self.method = environ["REQUEST_METHOD"]
        self.path = self.get_path("PATH_INFO")
        self.raw_path = self.get_path("RAW_URI")

        self.headers = {}
        self.cookies = {}

    @staticmethod
    def create_server(environ, start_response):
        WSGIServer.__server = WSGIServer(environ, start_response)

    @staticmethod
    def get_server():
        return WSGIServer.__server

    def send(self):
        try:
            return ["test".encode("utf-8")]
        finally:
            print("done")

    def get_path(self, key: str):
        referer_path = self.get_referer_path()

        return referer_path if referer_path else self.environ.get(key)

    def get_referer_path(self):
        return self.environ.get("HTTP_REFERER", None)
