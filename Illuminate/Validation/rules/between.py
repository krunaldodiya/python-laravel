from Illuminate.Validation.Rule import Rule


class Between(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self) -> bool:
        self.require_params_count(2)

        self.set_params({"small_value": self.args[0], "large_value": self.args[1]})

        small_value = self.params.get("small_value")

        large_value = self.params.get("large_value")

        value_length = self.get_size()

        return int(large_value) >= value_length >= int(small_value)

    def get_message(self) -> str:
        message = "The {field} field must be between {small_value} and {large_value}"

        return f"{message}." if self.is_numeric else f"{message} characters."
