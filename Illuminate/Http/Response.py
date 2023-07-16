import copy
import json


class Response:
    def __init__(self, app) -> None:
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

        await request.server.send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"application/json"],
                ],
            }
        )

        body = self.__app.get_container()

        stringify_body = json.dumps(body)

        await request.server.send(
            {
                "type": "http.response.body",
                "body": stringify_body.encode("utf-8"),
            }
        )
