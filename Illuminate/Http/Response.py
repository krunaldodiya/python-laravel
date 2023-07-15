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

    def send(self):
        return ["test".encode("utf-8")]
