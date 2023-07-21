from Illuminate.Routing.UrlGenerator import UrlGenerator


class Redirector:
    def __init__(self, app, url_generator: UrlGenerator) -> None:
        self.__app = app
        self.__url_generator = url_generator

        self.url = ""

    def to(self, url):
        self.url = url

        return self
