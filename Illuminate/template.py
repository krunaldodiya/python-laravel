from jinja2 import Environment, FileSystemLoader

from Illuminate.Support.Facades.Response import Response


class HtmlResponse:
    def __init__(self, data) -> None:
        self.data = data


class Template:
    def __init__(self, app) -> None:
        self.__app = app
        self.env = Environment(loader=FileSystemLoader("resources/views"))

    def make(self, file, args={}):
        template = self.env.get_template(f"{file}.html")
        data = template.render(**args)

        return Response.make(HtmlResponse(data=data), "200 OK")
