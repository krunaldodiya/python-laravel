class MiddlewareNameResolver:
    @classmethod
    def resolve(cls, name, middleware, middleware_groups):
        if isinstance(name, str):
            if middleware.get(name, None):
                return middleware.get(name)

            if middleware_groups.get(name, None):
                return middleware_groups.get(name, None)

        if hasattr(name, "handle"):
            return name

        return None
