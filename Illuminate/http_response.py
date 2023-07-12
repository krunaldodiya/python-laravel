import json

from Illuminate.template import HtmlResponse


class HttpResponse:
    def __init__(self) -> None:
        self.__response_body = ""
        self.__status = "200 OK"
        self.__response_headers = {"Content-type": "text/html"}

    @property
    def response_headers(self):
        return [(header[0], header[1]) for header in self.__response_headers.items()]

    @property
    def response_body(self):
        return self.__response_body

    @property
    def status(self):
        return self.__status

    def to_json(self):
        return json.dumps(self.response_body).encode("utf-8")

    def make(self, response_body, status):
        if type(response_body) == dict or type(response_body) == list:
            self.__response_body = json.dumps(response_body).encode("utf-8")
            self.__status = status
            self.__response_headers = {"Content-type": "application/json"}

        if type(response_body) == str:
            self.__response_body = response_body.encode("utf-8")
            self.__status = status
            self.__response_headers = {"Content-type": "text/plain"}

        if type(response_body) == HtmlResponse:
            self.__response_body = response_body.data.encode("utf-8")
            self.__status = status
            self.__response_headers = {"Content-type": "text/html"}

        return self
