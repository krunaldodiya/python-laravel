class Facade(type):
    def __getattr__(cls, method):
        facade_accessor = cls.get_facade_accessor()
        binding = cls.app.resolve(facade_accessor)
        return getattr(binding, method)
