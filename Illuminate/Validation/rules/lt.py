from Illuminate.Validation.Rule import Rule


class Lt(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(1)

        self.set_params({"lt": self.args[0]})

        lt = self.params.get("lt")

        value_length = self.get_size()

        return value_length < int(lt)

    def get_message(self) -> str:
        message = "The {field} field must less than {lt}"

        return f"{message}." if self.is_numeric else f"{message} characters."
