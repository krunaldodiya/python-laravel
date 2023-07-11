class Facade(type):
    def __getattr__(cls, method):
        facade_accessor = cls.get_facade_accessor()
        cls.application

        print(facade_accessor)

        return lambda route, handler: print(route, handler)
