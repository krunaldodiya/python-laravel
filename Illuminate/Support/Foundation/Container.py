class Container:
    def __init__(self) -> None:
        self.__bindings = {}
        self.__singletons = {}

    @property
    def bindings(self):
        return self.__bindings

    @property
    def singletons(self):
        return self.__singletons

    def make(self, key: str):
        return self.resolve(key)

    def bind(self, key: str, binding_resolver):
        self.set_binding(
            key,
            binding_resolver,
            False,
        )

    def singleton(self, key: str, binding_resolver):
        self.set_binding(
            key,
            binding_resolver,
            True,
        )

    def resolve(self, key: str):
        try:
            binding = self.bindings.get(key, None)

            if not binding:
                raise Exception("No binding found for.", key)

            binding_resolver = binding["binding_resolver"]

            is_singleton = binding["is_singleton"]

            if is_singleton:
                try:
                    singleton_instance = self.singletons[key]
                except KeyError:
                    singleton_instance = binding_resolver()
                    self.singletons[key] = singleton_instance

                return singleton_instance

            return binding_resolver()
        except Exception as e:
            raise Exception(e)

    def set_binding(self, key, binding_resolver, singleton):
        self.__bindings[key] = {
            "binding_resolver": binding_resolver,
            "is_singleton": singleton,
        }
