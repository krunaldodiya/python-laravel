from Illuminate.Validation.Rule import Rule


class Numeric(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        self.require_params_count(0)

        value = self.params.get("value")

        status, _ = self.is_numeric_value(value)

        return status

    def get_message(self) -> str:
        return "{field} must be a numeric value."
