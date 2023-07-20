from typing import TYPE_CHECKING, Any, Type

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class ResponseFactory:
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

        self.__content = ""
        self.__status = "200 OK"
        self.__headers = {"Content-type": "text/plain"}

    def get_status_code(self):
        return self.__status

    def get_headers(self):
        return [(key, value) for key, value in self.__headers.items()]

    def get_content(self):
        return self.__content

    def set_content(self, content: str):
        self.__content = content
        return self

    def set_status(self, status: str):
        self.__status = status
        return self

    def set_headers(self, key: str, value: Any):
        self.__headers[key] = value
        return self

    def send(self):
        request = self.__app.make("request")

        request.server.start_response(self.get_status_code(), self.get_headers())

        return [self.__content.encode("utf-8")]
