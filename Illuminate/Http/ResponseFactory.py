import asyncio
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class ResponseFactory:
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

    def send(self):
        pass

    async def send_async(self, server):
        await server.send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"application/json"],
                ],
            }
        )

        await server.send(
            {
                "type": "http.response.body",
                "body": "test".encode("utf-8"),
            }
        )
