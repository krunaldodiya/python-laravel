from Illuminate.Http.CookieBag import CookieBag
from Illuminate.Http.HeaderBag import HeaderBag


class ServerBag:
    def __init__(self, scope, receive, send) -> None:
        self.scope = scope
        self.receive = receive
        self.send = send

        self.client_url = self.__parse_url(scope["client"])
        self.server_url = self.__parse_url(scope["server"])

        self.client_host = scope["client"][0]
        self.client_port = scope["client"][1]

        self.server_host = scope["server"][0]
        self.server_port = scope["server"][1]

        self.scheme = scope["scheme"]
        self.query_string = scope["query_string"]
        self.method = scope["method"]
        self.root_path = scope["root_path"]
        self.path = scope["path"]
        self.raw_path = scope["raw_path"]

        self.headers = HeaderBag(scope["headers"])
        self.cookies = CookieBag(self.headers.headers["cookie"])

    def __parse_url(self, items: tuple):
        return ":".join(str(item) for item in items)
