class Facade(type):
    def __getattr__(cls, attribute, *args, **kwargs):
        from bootstrap.app import application

        facade_accessor = cls.get_facade_accessor()

        abstract = application.get_alias(facade_accessor)

        binding = application.make(abstract)

        return getattr(binding, attribute)
