from jinja2 import Environment, FileSystemLoader


class Template:
    def __init__(self) -> None:
        self.env = Environment(loader=FileSystemLoader("resources/views"))

    def make(self, file, args={}):
        template = self.env.get_template(f"{file}.html")

        return template.render(**args)
