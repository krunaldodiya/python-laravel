from Illuminate.Http.CookieBag import CookieBag
from Illuminate.Http.HeaderBag import HeaderBag


class ASGIServer:
    scope = None
    receive = None
    send = None

    @classmethod
    def init(cls, scope, receive, send) -> None:
        cls.scope = scope
        cls.receive = receive
        cls.send = send

    def create(self):
        self.client_url = self.__parse_url(self.scope["client"])
        self.server_url = self.__parse_url(self.scope["server"])

        self.client_host = self.scope["client"][0]
        self.client_port = self.scope["client"][1]

        self.server_host = self.scope["server"][0]
        self.server_port = self.scope["server"][1]

        self.scheme = self.scope["scheme"]
        self.query_string = self.scope["query_string"]
        self.method = self.scope["method"]
        self.path = self.scope["path"]
        self.raw_path = self.scope["raw_path"]

        self.headers = HeaderBag(self.scope["headers"])
        self.cookies = CookieBag(self.headers.headers["cookie"])

    def __parse_url(self, items: tuple):
        return ":".join(str(item) for item in items)
