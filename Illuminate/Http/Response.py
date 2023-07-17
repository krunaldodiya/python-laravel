import json

from typing import TYPE_CHECKING, Type
from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Foundation.Printer import Printer

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class Response:
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

        self.__response_body = ""
        self.__status = "200 OK"
        self.__response_headers = {"Content-type": "text/html"}

    def get_status_code(self):
        return "200 OK"

    def get_headers(self):
        return [("Content-type", "text/html")]

    def get_response_content(self):
        return "test".encode("utf-8")

    async def send(self):
        request = self.__app.make("request")

        kernel = self.__app.make(Kernel)

        router = self.__app.make("router")

        data = Printer(
            {
                "app": self.__app.__dict__,
                "kernel": kernel.__dict__,
                "router": router.__dict__,
            }
        )

        await request.server.send_response(
            {
                "status": 200,
                "headers": [
                    [b"content-type", b"application/json"],
                ],
                "body": json.dumps(data.print()).encode("utf-8"),
            }
        )
