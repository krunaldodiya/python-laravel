from typing import TYPE_CHECKING, Type


if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class Facade(type):
    app = None

    def __getattr__(cls, attribute, *args, **kwargs):
        facade_accessor = cls.get_facade_accessor()

        abstract = cls.app.get_alias(facade_accessor)

        binding = cls.app.make(abstract)

        return getattr(binding, attribute)

    @staticmethod
    def set_facade_application(app: Type["Application"]):
        Facade.app = app
