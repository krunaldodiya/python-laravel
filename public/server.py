class Server:
    def __init__(self, scope, receive, send) -> None:
        self.scope = scope
        self.receive = receive
        self.send = send

        self.client_url = self.__parse_url(scope["client"])
        self.server_url = self.__parse_url(scope["server"])

        self.http_host = scope["server"][0]
        self.server_port = scope["server"][1]

        self.query_string = scope["query_string"]
        self.request_method = scope["method"]

        self.headers = scope["headers"]

    async def send_response(self):
        assert self.scope["type"] == "http"

        await self.send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"text/plain"],
                ],
            }
        )

        await self.send(
            {
                "type": "http.response.body",
                "body": b"Hello, world!",
            }
        )

    def __parse_url(self, items: tuple):
        return ":".join(str(item) for item in items)
