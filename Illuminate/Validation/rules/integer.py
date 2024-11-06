from Illuminate.Validation.Rule import Rule


class Integer(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        self.require_params_count(0)

        value = self.params.get("value")

        return isinstance(value, int)

    def get_message(self) -> str:
        return "{field} must be a integer value."
