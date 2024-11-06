from Illuminate.Validation.Rule import Rule


class Gt(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(1)

        self.set_params({"gt": self.args[0]})

        gt = self.params.get("gt")

        value_length = self.get_size()

        return value_length > int(gt)

    def get_message(self) -> str:
        message = "The {field} field must greater than {gt}"

        return f"{message}." if self.is_numeric else f"{message} characters."
