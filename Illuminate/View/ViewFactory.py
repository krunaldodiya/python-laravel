from jinja2 import Environment, FileSystemLoader


class ViewFactory:
    def __init__(self, app) -> None:
        self.__app = app
        self.__env = Environment(loader=FileSystemLoader("resources/views"))
        self.__content = ""

    def make(self, file, args={}):
        template = self.__env.get_template(f"{file}.html")
        self.__content = template.render(**args)
        return self

    def get_content(self):
        return self.__content
