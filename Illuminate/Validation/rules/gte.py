from Illuminate.Validation.Rule import Rule


class Gte(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(1)

        self.set_params({"gte": self.args[0]})

        gte = self.params.get("gte")

        value_length = self.get_size()

        return value_length >= int(gte)

    def get_message(self) -> str:
        message = "The {field} field must greater than or equal to {gte}"

        return f"{message}." if self.is_numeric else f"{message} characters."
