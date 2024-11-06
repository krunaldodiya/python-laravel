from Illuminate.Validation.Rule import Rule


class Size(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        self.require_params_count(1)

        self.set_params({"size": self.args[0]})

        size = self.params.get("size")

        value_length = self.get_size()

        return value_length == int(size)

    def get_message(self) -> str:
        message = "The {field} field must be {size}"

        return f"{message}." if self.is_numeric else f"{message} characters."
