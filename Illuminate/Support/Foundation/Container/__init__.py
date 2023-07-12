class Container:
    def __init__(self) -> None:
        self.bindings = {}
        self.singletons = {}

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
        self.bindings[key] = {
            "binding_resolver": binding_resolver,
            "is_singleton": singleton,
        }

    def set_singleton(self, key, binding_resolver, singleton):
        self.set_binding(
            key=key,
            binding_resolver=binding_resolver,
            singleton=singleton,
        )
