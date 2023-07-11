class Router:
    def get(arg):
        print(arg)


class Facade(type):
    def __getattr__(cls, name):
        test = cls.get_facade_accessor()
        print(test)
        return Router.hello


class Route(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "route"


Route.get("test")
