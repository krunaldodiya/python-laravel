from Illuminate.Http.ServerBag.WSGIServer import WSGIServer


class Request:
    def __init__(self, server) -> None:
        self.server = server

        self.scheme = server.scheme
        self.server_name = server.server_name
        self.server_port = server.server_port
        self.host = server.host

        self.query_string = server.query_string
        self.method = server.method
        self.path = server.path
        self.raw_path = server.raw_path

        self.headers = server.headers
        self.cookies = server.cookies

    @staticmethod
    def capture():
        return Request.create_from_base(WSGIServer.get_server())

    @staticmethod
    def create_from_base(server):
        return Request(server)

    def get_host(self):
        return self.host

    def get_full_url(self):
        return f"{self.host}{self.path}"
