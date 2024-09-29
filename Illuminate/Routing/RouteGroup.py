class RouteGroup:
    @classmethod
    def merge(cls, new_attributes, old_attributes, prepend_existing_prefix=True):
        merged_group = {**old_attributes, **new_attributes}

        merged_group["prefix"] = cls._format_prefix(
            new_attributes, old_attributes, prepend_existing_prefix
        )

        return merged_group

    @classmethod
    def _format_prefix(
        cls, new_attributes, old_attributes, prepend_existing_prefix=True
    ):
        old_prefix: str = old_attributes.get("prefix", "")

        new_prefix: str = new_attributes.get("prefix", "")

        if prepend_existing_prefix:
            if new_prefix:
                return old_prefix.strip("/") + "/" + new_prefix.strip("/")

            return old_prefix

        return new_prefix.strip("/") + "/" + old_prefix.strip("/")
