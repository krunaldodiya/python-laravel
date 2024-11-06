from Illuminate.Validation.Rule import Rule


class Accepted(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.accepts = ["yes", "on", 1, "1", True, "true"]

    def validate(self):
        self.require_params_count(0)

        value = self.params.get("value")

        if self.value_exists(value):
            return value in self.accepts

        return False

    def get_message(self):
        return "The {field} field must be accepted"
