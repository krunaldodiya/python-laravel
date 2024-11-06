from Illuminate.Validation.Rule import Rule


class String(Rule):
    def __init__(self) -> None:
        super().__init__()

    def validate(self):
        self.require_params_count(0)

        value = self.params.get("value")

        return isinstance(value, str)

    def get_message(self):
        return "must be a string."
