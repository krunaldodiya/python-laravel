class Facade(type):
    def __getattr__(cls, attribute, *args, **kwargs):
        from wsgi import application

        facade_accessor = cls.get_facade_accessor()
        binding = application.make(facade_accessor)

        return getattr(binding, attribute)
