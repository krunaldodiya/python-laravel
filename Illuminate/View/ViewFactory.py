from jinja2 import Environment, FileSystemLoader


class ViewFactory:
    def __init__(self, app) -> None:
        self.__app = app
        self.__env = Environment(loader=FileSystemLoader("resources/views"))

    def make(self, file, args={}):
        template = self.__env.get_template(f"{file}.html")

        content = template.render(**args)

        response = self.__app.make("response")

        response = response.set_content(content)

        return "response"
