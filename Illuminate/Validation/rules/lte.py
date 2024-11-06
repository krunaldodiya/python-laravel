from Illuminate.Validation.Rule import Rule


class Lte(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(1)

        self.set_params({"lte": self.args[0]})

        lte = self.params.get("lte")

        value_length = self.get_size()

        return value_length < int(lte)

    def get_message(self) -> str:
        message = "The {field} field must less than {lte}"

        return f"{message}." if self.is_numeric else f"{message} characters."
