from Illuminate.Routing.UrlGenerator import UrlGenerator


class Redirector:
    def __init__(self, url_generator: UrlGenerator) -> None:
        self.__url_generator = url_generator
