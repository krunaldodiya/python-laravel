from Illuminate.Validation.Rule import Rule


class Max(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(1)

        self.set_params({"max": self.args[0]})

        max = self.params.get("max")

        value_length = self.get_size()

        return value_length <= int(max)

    def get_message(self) -> str:
        message = "The {field} field must not be greater than {max}"

        return f"{message}." if self.is_numeric else f"{message} characters."
