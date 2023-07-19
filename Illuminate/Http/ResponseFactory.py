from typing import TYPE_CHECKING, Type

from Illuminate.Support.Facades.Event import Event

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class ResponseFactory:
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

        self.__response_content = ""
        self.__status = "200 OK"
        self.__response_headers = {"Content-type": "text/html"}

    def get_status_code(self):
        return "200 OK"

    def get_headers(self):
        return [("Content-type", "text/html")]

    def get_response_content(self):
        return self.__response_content

    def send(self):
        pass

    def set_data(self, response_body):
        self.__response_content = response_body

    async def send_async(self, server):
        data = self.get_response_content()

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
                "body": data.encode("utf-8"),
            }
        )

        Event.dispatch("response_sent")
