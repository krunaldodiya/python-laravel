from typing import Any, Dict, List, Union


class MiddlewareNameResolver:
    @classmethod
    def resolve(
        cls,
        name: str,
        map: Dict[str, Any],
        middleware_groups: Dict[str, List[Union[str, Any]]],
    ):
        if isinstance(name, str):
            if name in map:
                return map[name]

            if name in middleware_groups:
                resolved_group = []

                for item in middleware_groups[name]:
                    if isinstance(item, str):
                        resolved_middleware = cls.resolve(item, map, middleware_groups)

                        if resolved_middleware:
                            resolved_group.append(resolved_middleware)
                    else:
                        resolved_group.append(item)

                return resolved_group

        if hasattr(name, "handle"):
            return name

        return None
