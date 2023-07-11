from jinja2 import Environment, FileSystemLoader


class View:
    def __init__(self) -> None:
        pass

    @staticmethod
    def make(file, args={}):
        env = Environment(loader=FileSystemLoader("resources/views"))

        template = env.get_template(f"{file}.html")

        return template.render(**args)
