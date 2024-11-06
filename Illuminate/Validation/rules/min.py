from Illuminate.Validation.Rule import Rule


class Min(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(1)

        self.set_params({"min": self.args[0]})

        min = self.params.get("min")

        value_length = self.get_size()

        return value_length >= int(min)

    def get_message(self) -> str:
        message = "The {field} field must be at least {min}"

        return f"{message}." if self.is_numeric else f"{message} characters."
