class Facade(type):
    def __getattr__(cls, attribute, *args, **kwargs):
        from bootstrap.app import app

        facade_accessor = cls.get_facade_accessor()

        abstract = app.get_alias(facade_accessor)

        binding = app.make(abstract)

        return getattr(binding, attribute)
