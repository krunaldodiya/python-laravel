class Server:
    def __init__(self, scope, receive, send, send_response) -> None:
        self.scope = scope
        self.receive = receive
        self.send = send
        self.send_response = send_response

        self.client_url = self.__parse_url(scope["client"])
        self.server_url = self.__parse_url(scope["server"])

        self.server_host = scope["server"][0]
        self.server_port = scope["server"][1]

        self.scheme = scope["scheme"]
        self.query_string = scope["query_string"]
        self.method = scope["method"]
        self.root_path = scope["root_path"]
        self.path = scope["path"]
        self.raw_path = scope["raw_path"]

        self.headers = scope["headers"]

    def __parse_url(self, items: tuple):
        return ":".join(str(item) for item in items)
